import os
from typing import List

import moviepy
import moviepy.editor

from zugswang.models import Scene

width = 1080
height = 1920 - 128


def generate_video(scenes: List[Scene], output_dir: str, pause_duration: float=0.5):
    os.makedirs(output_dir, exist_ok=True)

    canvas = moviepy.editor.ColorClip((width, height), col=(0, 0, 0))
    clips = []
    for i, scene in enumerate(scenes):
        clip = scene.generate_clip(i, canvas, output_dir, width, pause_duration)
        clips.append(clip)

    video = moviepy.editor.concatenate_videoclips(clips)
    video.write_videofile(os.path.join(output_dir, "final.mp4"), fps=24)


if __name__ == "__main__":
    from zugswang.puzzles.pins_001 import scenes
    output_dir = os.path.join("data", "puzzles", "pins_001")
    generate_video(scenes, output_dir)
