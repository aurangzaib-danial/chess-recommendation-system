import chess
import random
import copy
from math import log, sqrt, e, inf
import time

class MCTS:
  """
  Monte Carlo Tree Search Implementation for selecting chess pieces
  """
  def __init__(self, recommender, state, time_limit = 5, pieces = ['P','K','Q','B','N','R']):
    self._recommender = recommender
    self._pieces = pieces
    self._root_node = self.Node(state, pieces)
    self._time_limit = time_limit
    self._exploration_constant = 4

  def search(self):

    self._root_node.children = self._generate_children(self._root_node)

    start = time.time() 
    elapsed = 0  

    while elapsed < self._time_limit:
      
      expanded_child = self._expansion(self._root_node)

      node, reward = self._rollout(expanded_child)
     
      self._back_propagation(node, reward)

      elapsed = time.time() - start

    recommended_node = self._selection(self._root_node, exploration_constant = 0)

    final_node = self._expansion(recommended_node, exploration_constant = 0)

    return final_node.state

  def _ucb1(self, node, exploration_constant):
    """
    Returns Upper Confidence Bound for the given node.
    This function helps in deciding which node to evaluate next in MCTS.
    """
    exploited = node.score / (node.num_visited + (10**-10))
    explored = exploration_constant * sqrt(log(node.num_parent_visited+e+(10**-6)) / (node.num_visited + (10**-10)))
    # 10**-6 and 10**-10 are added to avoid 0 division exception.
    return exploited + explored

  def _selection(self, node, is_maximizer = True, exploration_constant = None):
    """
    Iterate through children of the given node and select the one
    with highest UCB value.
    """
    if exploration_constant == None:
      exploration_constant = self._exploration_constant
    
    selected_child = None

    best_value = -inf

    for child in node.children:
      node_value = self._ucb1(child, exploration_constant)

      if node_value > best_value:
        best_value = node_value
        selected_child = child

    return selected_child

  def _expansion(self, node, exploration_constant = None):
    """Expands the given node until leaf node is reached"""

    if len(node.children) == 0:
      return node # Leaf node reached

    selected_child = self._selection(node, exploration_constant)
    return self._expansion(selected_child, exploration_constant)

  def _rollout(self, node):
    """
    Recursively rollsout a node until all the open spots are filled out
    and then uses StockFish to determine statistics for the leaf node.
    """
    if "O" not in node.state:
      board = chess.Board(node.state)

      numWins, numStates = self._recommender.recurseStates(board)

      return node, float(numWins) / float(numStates)

    if len(node.children) == 0:
      node.children = self._generate_children(node)

    random_child = random.choice(list(node.children))

    return self._rollout(random_child)

  def _back_propagation(self, node, reward):
    """
    Traverses the reward till the root of the tree.
    This will update our UCB value of each node in the path.
    """
    while (node.parent != None):
      node.num_visited += 1
      node.score += reward
      node.num_parent_visited += 1
      node = node.parent


  def _generate_children(self, node):
    """
    Returns all the children for a node
    """
    children = set()

    number_of_empty_spots = node.state.count('O')

    if 'K' in node.state and 'K' in node.inventory:
      node.inventory.remove('K')

    if 'K' not in node.state and number_of_empty_spots == 1:
      children.add(self._generate_child(node, 'K'))
    else:
      for piece in node.inventory:
        children.add(self._generate_child(node, piece))

    return children


  def _generate_child(self, node, piece):
    temp_state = node.state.replace('O', piece, 1)
    child = self.Node(temp_state)
    child.parent = node
    child.inventory = copy.deepcopy(child.parent.inventory)
    child.inventory.remove(piece)
    return child

  # def _pieces(self):
  #   """
  #   Returns all the pieces that can placed in that position.
  #   I.E. a list like [P,K,Q,B,N,R]
  #   """
  #   return ['P','K','Q','B','N','R']


  class Node:
    """
    Represents a node in the game
    """
    def __init__(self, state = None, pieces = None):
      self.state = state # Current state of board
      self.children = set() # All possible states from current state
      self.parent = None
      self.inventory = copy.deepcopy(pieces)
      # Variables below are used in Upper Confidence Bound method
      self.num_parent_visited = 0 # N Number of times parent visited
      self.num_visited = 0 # n Number of times this node has been visited
      self.score = 0 # v Exploitation factor of node