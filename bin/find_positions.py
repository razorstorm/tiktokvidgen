import os

from dotenv import load_dotenv
import requests


load_dotenv()

RAPIDAPI_CHESS_PUZZLES_API_KEY = os.environ["RAPIDAPI_CHESS_PUZZLES_API_KEY"]
RAPIDAPI_CHESS_PUZZLES_API_HOST = os.environ["RAPIDAPI_CHESS_PUZZLES_API_HOST"]

url = f"https://{RAPIDAPI_CHESS_PUZZLES_API_HOST}/"
headers = {
    "x-rapidapi-key": RAPIDAPI_CHESS_PUZZLES_API_KEY,
    "x-rapidapi-host": RAPIDAPI_CHESS_PUZZLES_API_HOST,
}


def find_positions(themes):
    querystring = {
        "themes": "[" + ",".join([f'"{theme}"' for theme in themes]) + "]",
        "rating":"1000",
        "themesType":"ALL",
        "count":"10",
    }

    response = requests.get(url, headers=headers, params=querystring)
    positions = response.json()['puzzles']
    print(positions)


if __name__ == "__main__":
    find_positions(themes=["pin"])

[
    { 'puzzleid': 'PWywk', 'fen': '7b/1k4qP/2b2n2/1p1p4/pP1Q4/5P2/1PP5/1K5R b - - 2 40', 'rating': 1032, 'ratingdeviation': 93, 'moves': ['f6h7', 'd4g7', 'h8g7', 'h1h7'], 'themes': ['crushing', 'endgame', 'intermezzo', 'pin', 'short']},
    { 'puzzleid': 'oO3QH', 'fen': '3r2k1/2q2pp1/p6p/2p4P/Pp2N1R1/4P2K/1B1P2P1/8 b - - 4 33', 'rating': 1057, 'ratingdeviation': 81, 'moves': ['c7d7', 'e4f6', 'g8h8', 'f6d7'], 'themes': ['crushing', 'endgame', 'pin', 'short']},
    { 'puzzleid': 'SdHDy', 'fen': 'q5k1/p2R2p1/1p3r1p/2p1p3/3n4/3Q4/PP3PPP/3R2K1 w - - 0 25', 'rating': 934, 'ratingdeviation': 81, 'moves': ['d3g3', 'd4e2', 'g1f1', 'e2g3'], 'themes': ['crushing', 'endgame', 'fork', 'pin', 'short']},
    { 'puzzleid': 'dSH1Z', 'fen': 'kr6/prp5/4N1pp/1b1Qp3/3P4/4q3/PP4RK/8 b - - 1 33', 'rating': 989, 'ratingdeviation': 86, 'moves': ['b5f1', 'e6c7'], 'themes': ['mate', 'mateIn1', 'middlegame', 'oneMove', 'pin', 'smotheredMate']},
    { 'puzzleid': 'ydfYh', 'fen': '8/6k1/p6p/8/P7/5qPB/3R3K/8 b - - 1 51', 'rating': 941, 'ratingdeviation': 77, 'moves': ['f3f7', 'd2d7', 'g7f6', 'd7f7'], 'themes': ['crushing', 'endgame', 'master', 'pin', 'short']},
    { 'puzzleid': 'BnW47', 'fen': '8/1b6/p4p2/k1r2P2/8/3Q4/1P4qP/6RK w - - 0 42', 'rating': 993, 'ratingdeviation': 89, 'moves': ['g1g2', 'c5c1', 'd3f1', 'c1f1'], 'themes': ['endgame', 'mate', 'mateIn2', 'pin', 'short']},
    { 'puzzleid': 'yjerX', 'fen': 'r1b2rk1/ppq2ppp/4p3/2np2P1/5P2/P7/1PPQNP1P/2KR1BR1 w - - 0 18', 'rating': 1017, 'ratingdeviation': 76, 'moves': ['h2h4', 'c5b3', 'c1b1', 'b3d2'], 'themes': ['crushing', 'middlegame', 'pin', 'queensideAttack', 'short']},
    { 'puzzleid': 'oZFb4', 'fen': 'r1bknQ2/pp6/3p4/6P1/3pP3/5P2/Pq6/RN1nK1NR w - - 6 25', 'rating': 1031, 'ratingdeviation': 85, 'moves': ['e1d1', 'b2a1', 'h1h7', 'a1b1'], 'themes': ['advantage', 'hangingPiece', 'middlegame', 'pin', 'short']},
    { 'puzzleid': 'qcfzm', 'fen': '4r3/5k2/p3p3/1p1bQ1pP/8/1P6/P7/6K1 w - - 0 45', 'rating': 1013, 'ratingdeviation': 89, 'moves': ['e5g5', 'e8g8', 'g5g8', 'f7g8'], 'themes': ['crushing', 'endgame', 'pin', 'short']},
    { 'puzzleid': '4WazW', 'fen': 'r1b2rk1/pp3p2/3p2pp/q1pPb3/2B1P3/2N1Q2P/PP3PP1/R4RK1 w - - 0 16', 'rating': 1005, 'ratingdeviation': 87, 'moves': ['f2f4', 'e5d4', 'e3d4', 'c5d4'], 'themes': ['crushing', 'middlegame', 'pin', 'short']}
]
