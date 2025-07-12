"""
This classs is responsible for all the current state of the game and this is also responsible for the valid moves 
at this current state and also keep a move log.
"""

class GameState():
    def __init__(self):
        # board is a 8 by 8 2D list and each element of the list has 2 characters,
        # The first letter represents the color of the piece.
        # Second letter represents the what kind of piece.
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
        ]
        self.WhiteToMove = True
        self.moveLog = []