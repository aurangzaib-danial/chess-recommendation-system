import chess
import chess.engine
from lib.recommender import Recommender
from lib.helper import Helper

engine = chess.engine.SimpleEngine.popen_uci("stockfish")
recommender = Recommender(engine)

"""Inputs to the Application
coordinates is the state of the board in FEN encoding where empty spots are represented by 'O' character
pieces is the list available pieces, multiple same letters means there are multiple pieces of that type available
the time limit, limits how long MCTS will run. 
"""
layouts = [
    '5O2/8/4ppp1/5k2/5b2/5O2/8/O4N2',                # 5N2/8/4ppp1/5k2/5b2/5R2/8/K4Q2
    '6K1/3r3r/5kn1/5p2/5P2/6O1/8/4O1O1',             # 6K1/3r3r/5kn1/5p2/5P2/6N1/8/4R1R1
    '3n3k/2O5/2n1P3/3N2O1/8/1p6/2r3r1/K7',           # 3n3k/2R5/2n1P3/3N2N1/8/1p6/2r3r1/K7
    'rr4k1/6pp/2O5/3KO3/q7/8/8/8',                   # rr4k1/6pp/2Q5/3KN3/q7/8/8/8
    '4qrk1/6p1/5pP1/3K4/8/8/4P3/3O1O1O',             # 4qrk1/6p1/5pP1/3K4/8/8/4P3/3Q1R1R
    'rn3r1k/6pp/1pO2p2/p3O3/1P5q/PQ2PPp1/5n2/2O3K1', # rn3r1k/6pp/1pN2p2/p3N3/1P5q/PQ2PPp1/5n2/2R3K1
    '8/1p5p/pkp3r1/5O2/1P5O/7P/1q4P1/R6K',           # 8/1p5p/pkp3r1/5Q2/1P5B/7P/1q4P1/R6K
    '1r6/6kp/6p1/5RO1/8/P1P1p3/KO6/2q5',             # 1r6/6kp/6p1/5RQ1/8/P1P1p3/KP6/2q5
]

# get user input for puzzle selection
coordinates = Helper.userInput(layouts)
timeLimit = 10*coordinates.count('O')
pieces = ['P','K','Q','B','N','R']

print(Helper.printableBoard(coordinates))

print("\nGetting recommendation for the spots marked as O\n")

recommendation = recommender.recommend(coordinates, timeLimit, pieces)

print(chess.Board(recommendation))

engine.quit()