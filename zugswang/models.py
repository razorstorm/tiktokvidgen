import copy
from dataclasses import dataclass, field
import hashlib
import json
import os
from typing import Iterable, List, Optional, Tuple, Union

import chess
import chess.svg
# import cairosvg
import inspect
import moviepy
import moviepy.editor
import moviepy.video.fx.all as vfx
from PIL import Image
import numpy as np

from zugswang.elevenlabs import generate_audio_from_text, generate_audio_with_timestamps_from_text

narrations_dir = os.path.join("data", "narrations")
narrations_with_timestamp_dir = os.path.join("data", "narrations_with_timestamps")


@dataclass
class Puzzle:
    puzzleid: str
    fen: str
    rating: int
    ratingdeviation: int
    moves: List[str]
    themes: List[str]

    @property
    def difficulty(self):
        if self.rating < 1200:
            return "easy"
        elif self.rating < 1800:
            return "medium"
        elif self.rating < 2400:
            return "hard"
        elif self.rating < 3000:
            return "master"
        elif self.rating < 4000:
            return "grandmaster"
        else:
            return "?"

    @property
    def orientation(self):
        return chess.WHITE if self.fen.split()[1] == "b" else chess.BLACK


@dataclass
class Narration:
    text: str
    voice_id: str
    audio_path: str

    def __init__(self, text: str, voice_id: str="EODKX28NbkUPd7QWJ7yr"):
        self.text = text
        self.voice_id = voice_id
        audio_hash = hashlib.sha256(self.text.encode()).hexdigest()
        self.audio_path = os.path.join(narrations_with_timestamp_dir, voice_id, f"{audio_hash}.mp3")
        self.timestamp_path = os.path.join(narrations_with_timestamp_dir, voice_id, f"{audio_hash}.json")
        self.processed_timestamp_path = os.path.join(narrations_with_timestamp_dir, voice_id, f"{audio_hash}_processed.json")
        os.makedirs(os.path.dirname(self.audio_path), exist_ok=True)

        if not os.path.exists(self.audio_path) or not os.path.exists(self.timestamp_path):
            print("File not found")
            print("Text:")
            print(self.text)
            print("Audio Hash")
            print(audio_hash)
            print("----------------------")
            # print("Are you sure you are in the right folder?")
            generate_audio_with_timestamps_from_text(text, self.audio_path, self.timestamp_path, voice_id)
 
            # We need to convert these timestamps from character based to word based
        if not os.path.exists(self.processed_timestamp_path):
            self.start_times_dict = self.process_timestamps()
        else:
            with open(self.processed_timestamp_path, "r") as f:
                data = f.read()
                self.start_times_dict = json.loads(data)
        self.words = self.start_times_dict["words"]
        self.start_times = self.start_times_dict["start_times"]
        self.end_times = self.start_times_dict["end_times"]
    
    def process_timestamps(self) -> dict[str, list[str | float]]:
        timestamp_dict: dict = {}
        with open(self.timestamp_path, 'r') as f:
            data = f.read()
            timestamp_dict = json.loads(data)
        characters = timestamp_dict['characters']
        start_times = timestamp_dict['character_start_times_seconds']
        end_times = timestamp_dict['character_end_times_seconds']
        
        words = []
        word_start_times = []
        word_end_times = []
        current_word:str = None
        current_word_start_time = None
        total_characters = len(characters)
        index = 0
        
        for char, start_time, end_time in zip(characters, start_times, end_times):
            if char == " " or index >= total_characters - 1:
                if char != " ":
                    current_word += char
                if current_word is not None:
                    words.append(current_word)
                    word_start_times.append(current_word_start_time)
                    word_end_times.append(end_time)

                current_word = None
                current_word_start_time = None
            else:
                if not current_word:
                    current_word = char
                    current_word_start_time = start_time
                else:
                    current_word += char
            index += 1

        result = {
            "words": words,
            "start_times": word_start_times,
            "end_times": word_end_times,
        }
        
        with open(self.processed_timestamp_path, 'w') as f:
            f.write(json.dumps(result))
        
        return result    
        

@dataclass
class Scene:
    name: str
    narration: Narration
    media_filepath: str
    duration: float 
    caption: str
    
    def generate_caption_clips(self, width):
        if not self.caption:
            caption_clips = []
            for word, start_time, end_time in zip(self.narration.words, self.narration.start_times, self.narration.end_times):
                caption_clip = (
                    moviepy.editor.TextClip(
                        word, fontsize=150, align="Center", font="Bebas Neue Pro", color="white", method="caption", size=(width*0.8, None)
                    )
                    .set_start(start_time, change_end=False)
                    .set_end(end_time)
                    .set_position(["center", 1450])
                    # .crossfadein(duration=0.25)
                    # .crossfadeout(duration=0.25)
                )
                caption_clips.append(caption_clip)
            return caption_clips
        else:
            caption_clip = moviepy.editor.TextClip(self.caption, fontsize=65, align="West", font="Bebas Neue Pro", color="white", method="caption", size=(width*0.8, None))
    
    def generate_audio_clip(self, pause_duration):
        if not self.caption:
            narration_clip = moviepy.editor.AudioFileClip(self.narration.audio_path)
            pause_clip = moviepy.editor.AudioClip(lambda t: 0, duration=pause_duration)
            audio_clip = moviepy.editor.concatenate_audioclips([narration_clip, pause_clip])
            
            return audio_clip
        else:
            pause_clip = moviepy.editor.AudioClip(lambda t: 0, duration=self.duration)
            return pause_clip
        
    def generate_clip(self, id, output_dir, width: int, height: int, pause_duration: float=0.25):
        audio_clip = self.generate_audio_clip(pause_duration)

        image_clip = (
            moviepy.editor.ImageClip(self.media_filepath)
            .fl_image(lambda image: np.array(Image.fromarray(image).convert('RGB')))  # sometimes the image is missing a channel (?)
            .fx(vfx.resize, width=width*0.85)
            .set_duration(audio_clip.duration)
        )
        title_bg_color_clip = (
            moviepy.editor.ColorClip(size=(width, 180), color=[0,0,0,127.5])
            .set_duration(audio_clip.duration)
        )
        title_clip = (
            moviepy.editor.TextClip(self.name, fontsize=60, font="Bebas Neue Pro", color="white", bg_color="rgba(0,0,0,0)", method="caption", size=(width, None))
            .set_duration(audio_clip.duration)
        )
        # caption_clip = moviepy.editor.TextClip(self.narration.text, fontsize=65, align="West", font="Bebas Neue Pro", color="white", method="caption", size=(width*0.8, None))
        caption_clips = self.generate_caption_clips(width)
        
        scene_clip = moviepy.editor.CompositeVideoClip(
            [
                title_bg_color_clip.set_position("top"),
                title_clip.set_position(["center", 50]).crossfadein(duration=1).crossfadeout(duration=1),
                image_clip.set_position(["center", 500]).crossfadein(duration=1).crossfadeout(duration=1),
            ] + caption_clips,
            size=(width, height),
        )
        scene_clip = scene_clip.set_audio(audio_clip)
        scene_clip = scene_clip.set_duration(audio_clip.duration)
        scene_clip.write_videofile(os.path.join(output_dir, f"{id}.mp4"), fps=24)

        return scene_clip


@dataclass
class ChessScene:
    name: str
    narration: Narration
    board: chess.Board
    arrows: Iterable[Union[chess.svg.Arrow, Tuple[chess.Square, chess.Square]]]
    orientation: Optional[chess.Color]
    lastmove: Optional[chess.Move]

    def __init__(self, name, narration, board, arrows, orientation=chess.WHITE, lastmove=None):
        self.name = name
        self.narration = narration
        self.board = copy.deepcopy(board)
        self.arrows = arrows
        self.orientation = orientation
        self.lastmove = copy.deepcopy(lastmove)

    def generate_svg(self, size):
        svg = chess.svg.board(
            board=self.board,
            orientation=self.orientation,
            arrows=self.arrows,
            lastmove=self.lastmove,
            size=size,
            colors={
                "margin": "#000000",
                "outer border": "#000000",
            },
        )
        return svg
    
    def generate_clip(self, id, canvas, output_dir, width, pause_duration):
        pass
        # svg_path = os.path.join(output_dir, f"{id}.png")
        # svg = self.generate_svg(size=width)
        # cairosvg.svg2png(bytestring=svg, write_to=svg_path)

        # narration_clip = moviepy.editor.AudioFileClip(self.narration.audio_path)
        # pause_clip = moviepy.editor.AudioClip(lambda t: 0, duration=pause_duration)
        # audio_clip = moviepy.editor.concatenate_audioclips([narration_clip, pause_clip])
        # board_clip = moviepy.editor.ImageClip(svg_path)
        # title_clip = moviepy.editor.TextClip(self.name, fontsize=54, color="white", method="caption", size=(width, None))
        # caption_clip = moviepy.editor.TextClip(self.narration.text, fontsize=36, color="white", method="caption", size=(width, None))
        # scene_clip = moviepy.editor.CompositeVideoClip(
        #     [
        #         canvas,
        #         board_clip.set_position((0, 64)),
        #         title_clip.set_position((0, 64 + width + 64)),
        #         caption_clip.set_position((0, 64 + width + 64 + title_clip.size[1] + 64)),
        #     ],
        #     size=canvas.size
        # )
        # scene_clip = scene_clip.set_audio(audio_clip)
        # scene_clip = scene_clip.set_duration(audio_clip.duration)
        # scene_clip.write_videofile(os.path.join(output_dir, f"{id}.mp4"), fps=24)

        # return scene_clip


@dataclass
class Quiz:
    pass


@dataclass
class Walkthrough:
    pass
