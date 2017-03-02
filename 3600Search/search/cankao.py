# searchAgents.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
This file contains all of the agents that can be selected to 
control Pacman.  To select an agent, use the '-p' option
when running pacman.py.  Arguments can be passed to your agent
using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:
> python pacman.py -p SearchAgent -a searchFunction=depthFirstSearch
Commands to invoke other search strategies can be found in the 
project description.
Please only change the parts of the file you are asked to.
Look for the lines that say
"*** YOUR CODE HERE ***"
The parts you fill in start about 3/4 of the way down.  Follow the
project description for details.
Good luck and happy searching!
"""
from game import Directions
from game import Agent
from game import Actions
import util
import time
import search
import searchAgents

class GoWestAgent(Agent):
  "An agent that goes West until it can't."
  
  def getAction(self, state):
    "The agent receives a GameState (defined in pacman.py)."
    if Directions.WEST in state.getLegalPacmanActions():
      return Directions.WEST
    else:
      return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
  """
  This very general search agent finds a path using a supplied search algorithm for a
  supplied search problem, then returns actions to follow that path.
  
  As a default, this agent runs DFS on a PositionSearchProblem to find location (1,1)
  
  Options for fn include:
    depthFirstSearch or dfs
    breadthFirstSearch or bfs
    
  
  Note: You should NOT change any code in SearchAgent
  """
    
  def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
    # Warning: some advanced Python magic is employed below to find the right functions and problems
    
    # Get the search function from the name and heuristic
    if fn not in dir(search): 
      raise AttributeError, fn + ' is not a search function in search.py.'
    func = getattr(search, fn)
    if 'heuristic' not in func.func_code.co_varnames:
      print('[SearchAgent] using function ' + fn) 
      self.searchFunction = func
    else:
      if heuristic in dir(searchAgents):
        heur = getattr(searchAgents, heuristic)
      elif heuristic in dir(search):
        heur = getattr(search, heuristic)
      else:
        raise AttributeError, heuristic + ' is not a function in searchAgents.py or search.py.'
      print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic)) 
      # Note: this bit of Python trickery combines the search algorithm and the heuristic
      self.searchFunction = lambda x: func(x, heuristic=heur)
      
    # Get the search problem type from the name
    if prob not in dir(searchAgents) or not prob.endswith('Problem'): 
      raise AttributeError, prob + ' is not a search problem type in SearchAgents.py.'
    self.searchType = getattr(searchAgents, prob)
    print('[SearchAgent] using problem type ' + prob) 
    
  def registerInitialState(self, state):
    """
    This is the first time that the agent sees the layout of the game board. Here, we
    choose a path to the goal.  In this phase, the agent should compute the path to the
    goal and store it in a local variable.  All of the work is done in this method!
    
    state: a GameState object (pacman.py)
    """
    if self.searchFunction == None: raise Exception, "No search function provided for SearchAgent"
    starttime = time.time()
    problem = self.searchType(state) # Makes a new search problem
    self.actions  = self.searchFunction(problem) # Find a path
    totalCost = problem.getCostOfActions(self.actions)
    print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
    if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)
    
  def getAction(self, state):
    """
    Returns the next action in the path chosen earlier (in registerInitialState).  Return
    Directions.STOP if there is no further action to take.
    
    state: a GameState object (pacman.py)
    """
    if 'actionIndex' not in dir(self): self.actionIndex = 0
    i = self.actionIndex
    self.actionIndex += 1
    if i < len(self.actions):
      return self.actions[i]    
    else:
      return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
  """
  A search problem defines: 
  1. state space, 
  2. start state, 
  3. goal test,
  4. successor function
  5. cost function.  
  
  This search problem can be used to find paths to a particular 
  point on the pacman board.
  
  The state space consists of (x,y) positions in a pacman game.
  
  Note: this search problem is fully specified; you should NOT change it.
  """
  
  def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True):
    """
    Stores the start and goal.  
    
    gameState: A GameState object (pacman.py)
    costFn: A function from a search state (tuple) to a non-negative number
    goal: A position in the gameState
    """
    self.walls = gameState.getWalls()
    self.startState = gameState.getPacmanPosition()
    if start != None: self.startState = start
    self.goal = goal
    self.costFn = costFn
    if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
      print 'Warning: this does not look like a regular search maze'

    # For display purposes
    self._visited, self._visitedlist, self._expanded = {}, [], 0

  def getStartState(self):
    return self.startState

  def isGoalState(self, state):
     isGoal = state == self.goal 
     
     # For display purposes only
     if isGoal:
       self._visitedlist.append(state)
       import __main__
       if '_display' in dir(__main__):
         if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
           __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable
       
     return isGoal   
   
  def getSuccessors(self, state):
    """
    Returns successor states, the actions they require, and a cost of 1.
    
     As noted in search.py:
         For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
    """
    
    successors = []
    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      x,y = state
      dx, dy = Actions.directionToVector(action)
      nextx, nexty = int(x + dx), int(y + dy)
      if not self.walls[nextx][nexty]:
        nextState = (nextx, nexty)
        cost = self.costFn(nextState)
        successors.append( ( nextState, action, cost) )
        
    # Bookkeeping for display purposes
    self._expanded += 1 
    if state not in self._visited:
      self._visited[state] = True
      self._visitedlist.append(state)
      
    return successors

  def getCostOfActions(self, actions):
    """
    Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999
    """
    if actions == None: return 999999
    x,y= self.getStartState()
    cost = 0
    for action in actions:
      # Check figure out the next state and see whether its' legal
      dx, dy = Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]: return 999999
      cost += self.costFn((x,y))
    return cost

class StayEastSearchAgent(SearchAgent):
  """
  An agent for position search with a cost function that penalizes being in
  positions on the West side of the board.  
  
  The cost function for stepping into a position (x,y) is 1/2^x.
  """
  def __init__(self):
      self.searchFunction = search.uniformCostSearch
      costFn = lambda pos: .5 ** pos[0] 
      self.searchType = lambda state: PositionSearchProblem(state, costFn)
      
class StayWestSearchAgent(SearchAgent):
  """
  An agent for position search with a cost function that penalizes being in
  positions on the East side of the board.  
  
  The cost function for stepping into a position (x,y) is 2^x.
  """
  def __init__(self):
      self.searchFunction = search.uniformCostSearch
      costFn = lambda pos: 2 ** pos[0] 
      self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
  "The Manhattan distance heuristic for a PositionSearchProblem"
  xy1 = position
  xy2 = problem.goal
  return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
  "The Euclidean distance heuristic for a PositionSearchProblem"
  xy1 = position
  xy2 = problem.goal
  return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class CornersProblem(search.SearchProblem):
  """
  This search problem finds paths through all four corners of a layout.
  You must select a suitable state space and successor function
  """
  
  #startingGameState is of type gameState (defined in 
  # file pacman.py
  def __init__(self, startingGameState, costFn = lambda x: 1):
    """
    Stores the walls, pacman's starting position and corners.
    State format: [current_position, list_of_visited_corners, total_path_cost_from_start_to_n)
    current_position: (x, y)
    list_of_visited_corners: [1/0,1/0,1/0,1/0,]
    total_path_cost_from_start_to_n = int
    
    """
    self.walls = startingGameState.getWalls()
    self.startingPosition = startingGameState.getPacmanPosition()
    top, right = self.walls.height-2, self.walls.width-2 
    self.corners = ((1,1), (1,top), (right, 1), (right, top))
    self.goal = self.corners;
    self.costFn = costFn
    for corner in self.corners:
      if not startingGameState.hasFood(*corner):
        print 'Warning: no food in corner ' + str(corner)
    self._expanded = 0 # Number of search nodes expanded
    "*** YOUR CODE HERE ***"
    self._visited, self._visitedlist = {}, []
    self.startState = self.makeStartState()
    
  #states are now a tuple of type (position, [boolean values indicating visited corners])
  #For example if pacman is at location (3, 2) and on his current path he has visited corner (1,1)
  # the state would be ((3,2), [True, False, False, False])
  def makeStartState(self):
    startPos = self.startingPosition
    cornersVisited = [False, False, False, False];
    #check if start pos is in a corner
    for corner in range(len(self.corners)): 
        if startPos is self.corners[corner]:
            cornersVisited[corner] = True
            
    totalPathCost = 0
    startingPacmanState = ((startPos, cornersVisited, totalPathCost))
    return startingPacmanState

      
  #states are now a tuple of type (position, [boolean values indicating visited corners])
  #For example if pacman is at location (3, 2) and on his current path he has visited corner (1,1)
  # the state would be ((3,2), [True, False, False, False])
  def getStartState(self):
    "Returns the start state (in your state space, not the full Pacman state space)"
    "*** YOUR CODE HERE ***"
    return self.startState
    
  #goal state is any state where all corners are visited. So for all (x,y)
  # the state ((x, y), [True, True, True, True]) is a goal state
  def isGoalState(self, state):
    "Returns whether this search state is a goal state of the problem"
    "*** YOUR CODE HERE ***"

    if state[0] == self.goal[0]:
        state[1][0] = True
    if state[0] == self.goal[1]:
        state[1][1] = True
    if state[0] == self.goal[2]:
        state[1][2] = True
    if state[0] == self.goal[3]:
        state[1][3] = True
    if state[1][0] == True and state[1][1] ==  True and state[1][2] == True and state[1][3] == True:
        return True
    return False
       
  def getSuccessors(self, state):
    """
    Returns successor states, the actions they require, and a cost of 1.
    
     As noted in search.py:
         For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
    """
    
    successors = []
    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      # Add a successor state to the successor list if the action is legal
      # Here's a code snippet for figuring out whether a new position hits a wall:
      #currentPosition = state
      #x,y = currentPosition
      #dx, dy = Actions.directionToVector(action)
      #nextx, nexty = int(x + dx), int(y + dy)
      #hitsWall = self.walls[nextx][nexty]
      x,y = state[0]
      dx, dy = Actions.directionToVector(action)
      nextx, nexty = int(x + dx), int(y + dy)
      if not self.walls[nextx][nexty]:
        visited = []
        for i in range(len(state[1])):
            if state[1][i]:
                visited.append(True)
            else:
                visited.append(False)
                
        nextState = ((nextx, nexty),visited)
        cost = self.costFn(nextState)
        successors.append( ( nextState, action, cost) )
      "*** YOUR CODE HERE ***"
      
    self._expanded += 1
    if state[0] not in self._visited:
      self._visited[state[0]] = True
      self._visitedlist.append(state[0])
     
    return successors

  def getCostOfActions(self, actions):
    """
    Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999.  This is implemented for you.
    """
    if actions == None: return 999999
    x,y= self.startingPosition
    for action in actions:
      dx, dy = Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]: return 999999
    return len(actions)

#The algorithm for this heuristic is described in our readme.txt file
def cornersHeuristic(state, problem):
  """
  A heuristic for the CornersProblem that you defined.
  
    state:   The current search state 
             (a data structure you chose in your search problem)
    
    problem: The CornersProblem instance for this layout.  
    
  This function should always return a number that is a lower bound
  on the shortest path from the state to a goal of the problem; i.e.
  it should be admissible.  (You need not worry about consistency for
  this heuristic to receive full credit.)
  """
  corners = problem.corners # These are the corner coordinates
  walls = problem.walls # These are the walls of the maze, as a Grid (game.py)
  
  "*** YOUR CODE HERE ***"
  currentLocation = state[0] #pacman location

  goals = [] # goals is a list of unvisited goals.
  for i in range(len(problem.corners)):
      if not state[1][i]: #state of [1][i] = False if the goal has not been visited
          goals.append(problem.corners[i])
 
  accumulator = 0
  while len(goals) != 0: 
    j = findClosestCorner (currentLocation, goals)
    accumulator += findManhattanDistanceOfPairOfPoints(currentLocation, goals[j])
    currentLocation = goals[j] #move the current location to goal [j]
    goals.remove(goals[j]) # remove goal[j] from the list of unvisited goals
         
  return accumulator

# returns the Manhattan distance between point p1 and point p2
def findManhattanDistanceOfPairOfPoints(p1, p2):
    
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    dist = abs(x1 - x2) + abs(y1 - y2)
    return dist

#returns the index in food where the closest food is
def findClosestCorner(cur, corners):
    minDistIndex = -1
    minDist = -1
    for i in range(len(corners)):
        dist = findManhattanDistanceOfPairOfPoints(cur, corners[i])
        if dist!= 0 and (minDist == -1 or minDist >= dist):
            minDist = dist
            minDistIndex = i
    return minDistIndex

class AStarCornersAgent(SearchAgent):
  "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
  def __init__(self):
    self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
    self.searchType = CornersProblem


class AStarCornersAgent(SearchAgent):
  "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
  def __init__(self):
    self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
    self.searchType = CornersProblem

class FoodSearchProblem:
  """
  A search problem associated with finding the a path that collects all of the 
  food (dots) in a Pacman game.
  
  A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
    pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
    foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food 
  """
  def __init__(self, startingGameState):
    self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
    self.walls = startingGameState.getWalls()
    self.startingGameState = startingGameState
    self._expanded = 0
    self.heuristicInfo = {} # A dictionary for the heuristic to store information
      
  def getStartState(self):
    return self.start
  
  def isGoalState(self, state):
    return state[1].count() == 0

  def getSuccessors(self, state):
    "Returns successor states, the actions they require, and a cost of 1."
    successors = []
    self._expanded += 1
    for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      x,y = state[0]
      dx, dy = Actions.directionToVector(direction)
      nextx, nexty = int(x + dx), int(y + dy)
      if not self.walls[nextx][nexty]:
        nextFood = state[1].copy()
        nextFood[nextx][nexty] = False
        successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
    return successors

  def getCostOfActions(self, actions):
    """Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999"""
    x,y= self.getStartState()[0]
    cost = 0
    for action in actions:
      # figure out the next state and see whether it's legal
      dx, dy = Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]:
        return 999999
      cost += 1
    return cost

class AStarFoodSearchAgent(SearchAgent):
  "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
  def __init__(self):
    self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
    self.searchType = FoodSearchProblem

##########################################################################
def foodHeuristic(state, problem):
  """
  Path found with total cost of 60 in 353.5 seconds
  Search nodes expanded: 15683
  Pacman emerges victorious! Score: 570
  Your heuristic for the FoodSearchProblem goes here.
  
  This heuristic must be consistent to ensure correctness.  First, try to come up
  with an admissible heuristic; almost all admissible heuristics will be consistent
  as well.
  
  If using A* ever finds a solution that is worse uniform cost search finds,
  your heuristic is *not* consistent, and probably not admissible!  On the other hand,
  inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
  
  The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a 
  Grid (see game.py) of either True or False. You can call foodGrid.asList()
  to get a list of food coordinates instead.
  
  If you want access to info like walls, capsules, etc., you can query the problem.
  For example, problem.walls gives you a Grid of where the walls are.
  
  If you want to *store* information to be reused in other calls to the heuristic,
  there is a dictionary called problem.heuristicInfo that you can use. For example,
  if you only want to count the walls once and store that value, try:
    problem.heuristicInfo['wallCount'] = problem.walls.count()
  Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount']
  """
  return foodHelper (state)
  #return kruskal (state)

def manhattanDistance(p1, p2):
    return abs(p1[0] - p2[0]) + abs (p1[1] - p2[1])

def findMostDistantGoals(now, goals):
  maxDist = 0
  bestFirst = goals[0]
  bestSecond = goals[1]
  for i in range(len(goals)):
    thisGoal = goals.pop()
    if len(goals) > 0:
      for j in range(len(goals)):
        dist = manhattanDistance(thisGoal, goals[j])
        if dist > maxDist:
          maxDist = dist
          bestFirst = thisGoal
          bestSecond = goals[j]
    else: 
        return maxDist, bestFirst, bestSecond
###########################################################################
def foodHelper(state):
  corners = state[1].asList() # These are the corner coordinates
  
  "*** YOUR CODE HERE ***"
  currentLocation = state[0] #pacman location

  goals = [] # goals is a list of unvisited goals.
  for i in range(len(corners)):
    goals.append(corners[i])
 
  accumulator = 0
  largestDist = 0
  for i in range(len(goals)): 
    j = findClosestCorner (currentLocation, goals)
    distance = findManhattanDistanceOfPairOfPoints(currentLocation, goals[j])
    accumulator += distance
    currentLocation = goals[j] #move the current location to goal [j]
    if i != 0 and(largestDist == 0 or largestDist > distance):
        largestDist = distance
  
  accumulator = accumulator - largestDist       
  return accumulator

# Kruskal
def kruskal (state):
    goals = state[1].asList()
    curLoc = state[0]
    edgeAndNodes = sortGoals(curLoc, goals)
    nodes = [] #subgraph of the mst. Will contain triplets
    edgeSum = 0
    for i in range(len(edgeAndNodes)):
        #if the end points of e are disconnected in , add e to s
        curTriplet = edgeAndNodes[i]
        if not curTriplet[1] in nodes or not curTriplet[2] in nodes:
            edgeSum += curTriplet[0]
            # we don't care if nodes was missing curTriplet[1] or curTriplet[2]
            # because we only care whether a node is present in the set or not.
            # so we just always add both of them
            nodes.append(curTriplet[1])
            nodes.append(curTriplet[2])
    
    return edgeSum

# returns a sortd list of triplets. list is sorted by the 0th element
# triplet values (dist, node1, node2)
def sortGoals(curLoc, goals):
    allPoints = []
    allPoints.append(curLoc)
    for i in range(len(goals)):
        allPoints.append(goals[i])
    
    edgeAndNodes = []
    for i in range (len(allPoints)):
        for j in range(i, len(allPoints)):
            dist = findManhattanDistanceOfPairOfPoints(allPoints[i], allPoints[j])
            en =(dist, allPoints[i], allPoints[j])
            edgeAndNodes = insertEdgeAndNodes(en, edgeAndNodes)
    return edgeAndNodes

#inserts the triplet en into the right spot in edgeAndNodes
def insertEdgeAndNodes(en, edgeAndNodes):
    if len(edgeAndNodes) == 0:
        edgeAndNodes.append(en)
        return edgeAndNodes
    
    
    for i in range(len(edgeAndNodes)):
        curEn = edgeAndNodes
        curDist = curEn[0]
        if curDist > en[0]:
            edgeAndNodes.insert(i, en) #insert en before element i
            return edgeAndNodes
    #if we get to here without returning, the element must go at the end of the list
    edgeAndNodes.append(en)
    return edgeAndNodes
######################################################
  
class ClosestDotSearchAgent(SearchAgent):
  "Search for all food using a sequence of searches"
  def registerInitialState(self, state):
    self.actions = []
    currentState = state
    while(currentState.getFood().count() > 0): 
      nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
      self.actions += nextPathSegment
      for action in nextPathSegment: 
        legal = currentState.getLegalActions()
        if action not in legal: 
          t = (str(action), str(currentState))
          raise Exception, 'findPathToClosestDot returned an illegal move: %s!\n%s' % t
        currentState = currentState.generateSuccessor(0, action)
    self.actionIndex = 0
    print 'Path found with cost %d.' % len(self.actions)
    
  def findPathToClosestDot(self, gameState):
    "Returns a path (a list of actions) to the closest dot, starting from gameState"
    # Here are some useful elements of the startState
    startPosition = gameState.getPacmanPosition()
    food = gameState.getFood().asList()
    walls = gameState.getWalls()
    problem = AnyFoodSearchProblem(gameState)
    
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH
    
    "*** YOUR CODE HERE ***"
    path =  search.breadthFirstSearch(problem)
    
    return path
 
class AnyFoodSearchProblem(PositionSearchProblem):
  """
    A search problem for finding a path to any food.
    
    This search problem is just like the PositionSearchProblem, but
    has a different goal test, which you need to fill in below.  The
    state space and successor function do not need to be changed.
    
    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.
    
    You can use this search problem to help you fill in 
    the findPathToClosestDot method.
  """

  def __init__(self, gameState):
    "Stores information from the gameState.  You don't need to change this."
    # Store the food for later reference
    self.food = gameState.getFood()

    # Store info for the PositionSearchProblem (no need to change this)
    self.walls = gameState.getWalls()
    self.startState = gameState.getPacmanPosition()
    self.costFn = lambda x: 1
    self._visited, self._visitedlist, self._expanded = {}, [], 0
    
  def isGoalState(self, state):
    """
    The state is Pacman's position. Fill this in with a goal test
    that will complete the problem definition.
    """
    x,y = state
    "*** YOUR CODE HERE ***"
    food = self.food.asList()
    if state in food:
        return True
    return False

##################
# Mini-contest 1 #
##################

class ApproximateSearchAgent(Agent):
  "Implement your contest entry here.  Change anything but the class name."
  
  def registerInitialState(self, state):
    "This method is called before any moves are made."
    "*** YOUR CODE HERE ***"
    
  def getAction(self, state):
    """
    From game.py: 
    The Agent will receive a GameState and must return an action from 
    Directions.{North, South, East, West, Stop}
    """ 
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
    
def mazeDistance(point1, point2, gameState):
  """
  Returns the maze distance between any two points, using the search functions
  you have already built.  The gameState can be any game state -- Pacman's position
  in that state is ignored.
  
  Example usage: mazeDistance( (2,4), (5,6), gameState)
  
  This might be a useful helper function for your ApproximateSearchAgent.
  """
  x1, y1 = point1
  x2, y2 = point2
  walls = gameState.getWalls()
  assert not walls[x1][y1], 'point1 is a wall: ' + point1
  assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
  prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False)
  return len(search.bfs(prob))