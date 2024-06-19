from dataclasses import dataclass, field
import hashlib
import os
from typing import Iterable, List, Optional, Tuple, Union

import chess
import chess.svg

from zugswang.elevenlabs import generate_audio_from_text

narrations_dir = os.path.join("data", "narrations")


@dataclass
class Puzzle:
    puzzleid: str
    fen: str
    rating: int
    moves: List[str]
    themes: List[str]


@dataclass
class Narration:
    text: str
    voice_id: str
    audio_path: str

    def __init__(self, text: str, voice_id: str="uYkKk3J4lEp7IHQ8CLBi"):
        self.text = text
        self.voice_id = voice_id
        audio_hash = hashlib.sha256(text.encode()).hexdigest()
        self.audio_path = os.path.join(narrations_dir, voice_id, f"{audio_hash}.mp3")
        os.makedirs(os.path.dirname(self.audio_path), exist_ok=True)

        if not os.path.exists(self.audio_path):
            generate_audio_from_text(text, self.audio_path, voice_id)


@dataclass
class Scene:
    name: str
    narration: Narration
    board: chess.Board
    arrows: Iterable[Union[chess.svg.Arrow, Tuple[chess.Square, chess.Square]]]
    lastmove: Optional[chess.Move] = None

    def generate_svg(self, size):
        svg = chess.svg.board(
            board=self.board,
            arrows=self.arrows,
            lastmove=self.lastmove,
            size=size,
            colors={
                "margin": "#000000",
                "outer border": "#000000",
            },
        )
        return svg
