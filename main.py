import os
from typing import List

import cairosvg
import moviepy
import moviepy.editor

from zugswang.models import Scene

width = 1080
height = 1920


def generate_video(scenes: List[Scene], output_dir: str, pause_duration: float=0.5):
    os.makedirs(output_dir, exist_ok=True)

    canvas = moviepy.editor.ColorClip((width, height), col=(0, 0, 0))
    video_clips = []
    audio_clips = []
    for i, scene in enumerate(scenes):
        svg_path = os.path.join(output_dir, f"{i}.png")
        svg = scene.generate_svg(size=width)
        cairosvg.svg2png(bytestring=svg, write_to=svg_path)

        narration_clip = moviepy.editor.AudioFileClip(scene.narration.audio_path)
        pause_clip = moviepy.editor.AudioClip(lambda t: 0, duration=pause_duration)
        board_clip = moviepy.editor.ImageClip(svg_path)
        caption_clip = moviepy.editor.TextClip(scene.narration.text, fontsize=24, color="white", method="caption", size=(width, None))
        scene_clip = (moviepy.editor.CompositeVideoClip([canvas, board_clip, caption_clip.set_position((0, width + 64))], size=canvas.size)
                    .set_duration(narration_clip.duration + pause_duration))
        scene_clip.write_videofile(os.path.join(output_dir, f"{i}.mp4"), fps=24)

        video_clips.append(scene_clip)
        audio_clips.append(narration_clip)
        audio_clips.append(pause_clip)
    
    audio = moviepy.editor.concatenate_audioclips(audio_clips)
    video = moviepy.editor.concatenate_videoclips(video_clips).set_audio(audio)
    video.write_videofile(os.path.join(output_dir, "final.mp4"), fps=24)


if __name__ == "__main__":
    from zugswang.puzzles.pins_001 import scenes
    output_dir = os.path.join("data", "puzzles", "pins_001")
    generate_video(scenes, output_dir)
