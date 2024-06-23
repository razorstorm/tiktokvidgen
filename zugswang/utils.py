from typing import List

import chess
import chess.svg


def show_attacks(board, square) -> List[chess.svg.Arrow]:
    arrows = list()
    attackers = board.attackers(chess.BLACK if board.turn == chess.WHITE else chess.WHITE, square)
    defenders = board.attackers(chess.WHITE if board.turn == chess.WHITE else chess.BLACK, square)
    for attacker in attackers:
        arrows.append(chess.svg.Arrow(attacker, square, color="green"))
    for defender in defenders:
        arrows.append(chess.svg.Arrow(defender, square, color="red"))
    
    return arrows
