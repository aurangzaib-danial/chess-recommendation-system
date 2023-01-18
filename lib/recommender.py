from lib.mcts import MCTS
import chess

class Recommender:
  """
  This class is responsible for generating recommendations based on a given
  state using Stockfish and Monte Carlo Tree Search
  """

  def __init__(self, engine):
    self._engine = engine

  def recommend(self, state, timeLimit = 15, pieces = ['P','K','Q','B','N','R']):
    """
    Using MCTS for generating recommendation.
    Time limit is based on seconds.
    """
    if len(pieces) < state.count("0"):
      print("Not enough pieces to fill all open positions. Cannot make a good recommendation")
      return state
    return MCTS(self, state, timeLimit, pieces).search()

  def _getBestStates(self, state, numMoves = 3, timeLimit = 0.01):
    """
    Returns top three best next states by default for a given state.
    """
    info = self._engine.analyse(state, chess.engine.Limit(time=timeLimit), multipv=numMoves)
    bestStates = []
    for i in range(len(info)):
      newState = state.copy()
      newState.push(info[i]['pv'][0])
      bestStates.append(newState)
        
    return bestStates

  def recurseStates(self, state, depth = 3):
    """
    Returns the number of winning states and the number of states visited
    within a given depth.
    """
    numWins = 0
    numStates = 0
    if depth > 0:
      nextStates = self._getBestStates(state)
      for nextState in nextStates:
        numStates += 1
        if nextState.is_game_over():
          if nextState.result() == "1-0":
            numWins += 1
        else:
          x, y = self.recurseStates(nextState, depth-1)
          numWins += x
          numStates += y
    return numWins, numStates

