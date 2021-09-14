# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

#Import by me
from game import Grid

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        #print(scores)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()

        newFood = successorGameState.getFood()
        numFood = successorGameState.getNumFood()

        newGhostStates = successorGameState.getGhostStates()
        newGhostPos = successorGameState.getGhostPositions()

        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newCapsulePos = successorGameState.getCapsules()

        "*** YOUR CODE HERE ***"
        score = 0
        minDistToGhost = 999999
        for ghost in newGhostPos:
            temp = manhattanDistance(newPos, ghost)
            if temp < minDistToGhost:
                minDistToGhost = temp

            if temp <= 1 and not newScaredTimes[0]:
                score = -999999


        foodlist = newFood.asList()
        minDistToFood = 999999

        for i in foodlist:
            temp = manhattanDistance(newPos, i)

            if temp < minDistToFood:
                minDistToFood = temp

        distToCapsule = 0
        if len(newCapsulePos) != 0: #Capsule still available
            distToCapsule = manhattanDistance(newPos, newCapsulePos[0])

        if newScaredTimes[0] and (minDistToGhost != 0): #ghost scared
            score = score + 1/minDistToGhost*1000
            #distToCapsule = 0
        elif distToCapsule: #Capsule still available
            score = score + 1/minDistToFood + 1/distToCapsule*500 - numFood*100 #numFood needed to incentivise Pacman to eat
        else: #capsule already eaten
            score = score + 1/minDistToFood - numFood*100
        """
        print("successorGameState: ", successorGameState)
        print("newPos: ", newPos)
        print("newFood: ", )
        for i in newGhostPos:
            print("newGhostStates: ", i)
        #print("newScaredTimes: ", newScaredTimes)
        """
        return score
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
k
        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        maxNodeUtil = []
        #print("AgentNum:", numAgents)

        def __miniMax(state,iter):
            if iter >= self.depth*numAgents or state.isWin() or state.isLose(): #terminal states
                return self.evaluationFunction(state)
            elif iter%numAgents != 0: #Adversaries' turns
                v = 999999
                for action in state.getLegalActions(iter%numAgents):
                    s = state.generateSuccessor(iter%numAgents, action)
                    v = min(v, __miniMax(s, iter + 1))
                return v
            else: #Pacman's turn
                v = -999999
                for action in state.getLegalActions(self.index):
                    s = state.generateSuccessor(self.index, action)
                    v = max(v, __miniMax(s, iter + 1))
                    if iter == 0:
                        maxNodeUtil.append(v) # Min values following max won't be added onto the list.
                return v

        r = __miniMax(gameState, 0)
        #print("\n")
        #print("miniMax:", r)
        #print("maxList: ", maxNodeUtil)
        #print("\n")
        return  gameState.getLegalActions(self.index)[maxNodeUtil.index(max(maxNodeUtil))]
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        maxNodeUtil = []
        #print("AgentNum:", numAgents)

        def __alphaBeta(state,iter,alpha,beta):
            if iter >= self.depth*numAgents or state.isWin() or state.isLose(): #terminal states
                return self.evaluationFunction(state)
            elif iter%numAgents != 0: #Adversaries' turns
                v = 999999
                for action in state.getLegalActions(iter%numAgents):
                    s = state.generateSuccessor(iter%numAgents, action)
                    v = min(v, __alphaBeta(s, iter + 1, alpha, beta))
                    if v < alpha: return v
                    beta = min(v, beta)
                return v
            else: #Pacman's turn
                v = -999999
                for action in state.getLegalActions(self.index):
                    s = state.generateSuccessor(self.index, action)
                    v = max(v, __alphaBeta(s, iter + 1, alpha, beta))
                    if v > beta: return v
                    alpha = max(v, alpha)

                    if iter == 0:
                        maxNodeUtil.append(v) # Min values following max won't be added onto the list.
                return v

        r = __alphaBeta(gameState, 0, -999999, 999999)
        return gameState.getLegalActions(self.index)[maxNodeUtil.index(max(maxNodeUtil))]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        maxNodeUtil = []
        #print("AgentNum:", numAgents)

        def __ExpMax(state,iter):
            if iter >= self.depth*numAgents or state.isWin() or state.isLose(): #terminal states
                return self.evaluationFunction(state)
            elif iter%numAgents != 0: #Adversaries' turns
                mean = 0
                actions = state.getLegalActions(iter % numAgents)
                prob = 1 / len(actions)  # Assume equal probability for each move
                for action in actions:
                    s = state.generateSuccessor(iter%numAgents, action)
                    mean = mean + prob*__ExpMax(s, iter + 1)
                return mean
            else: #Pacman's turn
                v = -999999
                for action in state.getLegalActions(self.index):
                    s = state.generateSuccessor(self.index, action)
                    v = max(v, __ExpMax(s, iter + 1))
                    if iter == 0:
                        maxNodeUtil.append(v) # Min values following max won't be added onto the list.
                return v

        r = __ExpMax(gameState, 0)
        #print("\n")
        #print("miniMax:", r)
        #print("maxList: ", maxNodeUtil)
        #print("\n")
        return  gameState.getLegalActions(self.index)[maxNodeUtil.index(max(maxNodeUtil))]

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    Features:
        - number of food remaining. lower better
        - average distance to all ghosts
        - available actions. more freedom better
        - distance to capsule if still available
        - distance to closest food. shorter better
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()

    availMoves = len(currentGameState.getLegalPacmanActions())

    newFood = currentGameState.getFood() #food grid
    numFood = currentGameState.getNumFood()

    newGhostStates = currentGameState.getGhostStates()
    newGhostPos = currentGameState.getGhostPositions()

    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newCapsulePos = currentGameState.getCapsules()
    numOfCapsule = len(newCapsulePos)
    evalScore=0
    avgDistToGhost = 0
    for ghost in newGhostPos:
        avgDistToGhost = avgDistToGhost + manhattanDistance(newPos, ghost)

    avgDistToGhost = avgDistToGhost/len(newGhostPos)

    foodList = newFood.asList()
    minDistToFood = 999999
    maxDistToFood = -999999
    avgDistToFood = 0
    for i in foodList:
        temp =  manhattanDistance(newPos, i)
        avgDistToFood = avgDistToFood + temp
        if temp < minDistToFood:
            minDistToFood = temp

        if temp > maxDistToFood:
            maxDistToFood = temp

    avgScaredTIme = sum(newScaredTimes)/len(newScaredTimes)
    if newScaredTimes[0]:  # ghost scared
        evalScore = 5000/avgDistToGhost - numFood*400 + 300*1/minDistToFood
    elif numOfCapsule != 0:  # Capsule still available
        # = [manhattanDistance(newPos, cap) for cap in newCapsulePos]
        #distToCapsule = sum(temp)/numOfCapsule
        evalScore = 180*avgDistToGhost -numFood*500  + availMoves  + 300*1/minDistToFood -100*maxDistToFood - 250*numOfCapsule
    else:
        evalScore =  180*avgDistToGhost -numFood*500  + availMoves + 300*1/minDistToFood -100*maxDistToFood

    return evalScore

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
