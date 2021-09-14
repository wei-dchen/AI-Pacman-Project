# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState() # only x,y position
    fringed = util.Stack()
    fringed.push(start)
    visited = []
    parentMap = dict() # To keep track of a child's parent for printing out start -> goal path

    while (not fringed.isEmpty()):
        if (fringed.isEmpty()): return "Not Found!"
        node = fringed.pop()

        if problem.isGoalState(node) == True: return genPath(parentMap,node,start)

        if node not in visited:
            visited.append(node)
            for child_node,action,cost in problem.getSuccessors(node):
                # problem.getSuccessors(node) of type: (5, 4), 'South', 1)
                fringed.push(child_node)

                if child_node not in visited: # Check to not include parent that's already a child
                    parentMap[child_node] = (node,action)

    util.raiseNotDefined()

def genPath(parentMap,node,start):
    # return a list of actions form the start to goal
    paths = []
    if len(parentMap[node]) == 2:
        #print("map keys: ", parentMap.keys())
        while node != start: # has parents
            nodeTuple = parentMap[node]
            node,action = nodeTuple
            paths.append(action)
    else: # When parentMap includes cost, i.e. (node,action,updateCost). For A* and UCS
        while node != start: # has parents
            nodeTuple = parentMap[node]
            node,action,_ = nodeTuple
            paths.append(action)

    #print(listOfNodes[::-1]) # (listOfNodes.reverse()) <= doesn't work?
    return paths[::-1]


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState() # only x,y position
    fringed = util.Queue()
    fringed.push(start)
    visited = []
    parentMap = dict() # To keep track of a child's parent for printing out start -> goal path

    while (not fringed.isEmpty()):
        if (fringed.isEmpty()): return "Not Found!"
        node = fringed.pop() # Enqueue the start node

        if problem.isGoalState(node) == True: return genPath(parentMap,node,start)

        if node not in visited:
            visited.append(node)
            for child_node,action,cost in problem.getSuccessors(node):
                # problem.getSuccessors(node) of type: (5, 4), 'South', 1)
                if (child_node not in visited) and (child_node not in parentMap.keys()):
                    fringed.push(child_node)
                # Check to not include parent that's already a child
                    parentMap[child_node] = (node,action)

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState() # only x,y position
    fringed = util.PriorityQueue()
    fringed.push(start,0)
    visited = []
    parentMap = dict() # To keep track of a child's parent for printing out start -> goal path

    while (not fringed.isEmpty()):
        if (fringed.isEmpty()): return "Not Found!"
        node = fringed.pop() # Enqueue the start node

        if problem.isGoalState(node) == True: return genPath(parentMap,node,start)

        if node not in visited:
            visited.append(node)
            for child_node,action,cost in problem.getSuccessors(node):
                # problem.getSuccessors(node) of type: (5, 4), 'South', 1)
                if child_node in parentMap.keys() and ((parentMap[node][2] + cost) < parentMap[child_node][2]):
                    updateCost = parentMap[node][2] + cost
                    fringed.update(child_node,updateCost)
                    parentMap[child_node] = (node,action,updateCost)

                if (child_node not in visited) and (child_node not in parentMap.keys()):

                    # Calculate accumulated costs up a given node
                    fringedCost = 0
                    if node != start:
                        fringedCost = parentMap[node][2] + cost
                    else:
                        fringedCost = fringedCost + cost

                    fringed.push(child_node,fringedCost)
                    # Check to not include parent that's already a child
                    parentMap[child_node] = (node,action,fringedCost)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState() # only x,y position
    fringed = util.PriorityQueue()
    fringed.push(start,0)
    visited = []
    parentMap = dict() # To keep track of a child's parent for printing out start -> goal path

    while (not fringed.isEmpty()):
        if (fringed.isEmpty()): return "Not Found!"
        node = fringed.pop() # Enqueue the start node

        if problem.isGoalState(node) == True: return genPath(parentMap,node,start)

        if node not in visited:
            visited.append(node)
            for child_node,action,cost in problem.getSuccessors(node):
                # problem.getSuccessors(node) of type: (5, 4), 'South', 1)
                heuristicCost = heuristic(child_node,problem)

                if child_node in parentMap.keys() and ((parentMap[node][2] + cost) < parentMap[child_node][2]):
                    updateCost = parentMap[node][2] + cost
                    fringed.update(child_node,updateCost+heuristicCost)
                    parentMap[child_node] = (node,action,updateCost)
                    continue

                if (child_node not in visited) and (child_node not in parentMap.keys()):

                    # Calculate accumulated costs  up a given node
                    fringedCost = 0
                    if node != start:
                        fringedCost = parentMap[node][2] + cost
                    else:
                        fringedCost = fringedCost + cost

                    fringed.push(child_node,fringedCost+heuristicCost)
                    # Check to not include parent that's already a child
                    parentMap[child_node] = (node,action,fringedCost)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
