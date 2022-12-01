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


from unittest import result
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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

        "*** YOUR CODE HERE ***"
        nearestFood = float('inf')

        if not newFood.asList():
            nearestFood = 0
        for food in newFood.asList():
            nearestFood = min(nearestFood, manhattanDistance(food, newPos))

        hero = -0.5 * nearestFood + successorGameState.getScore() 
        return hero

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

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
        return self.agentAction(gameState, agentIndex=0, depth=self.depth)[1]

    def agentAction(self, gameState, agentIndex, depth):
        # Hero
        if agentIndex == 0:
            return self.agentZero(gameState, agentIndex, depth)

        # Ghost
        else:
            return self.agentGhost(gameState, agentIndex, depth)

    def agentZero (self, gameState, agentIndex, depth):
        if (gameState.isWin() or gameState.isLose() or depth == 0):
            return self.evaluationFunction(gameState), None
        legalMoves = gameState.getLegalActions(agentIndex)
        heroScore = -float("inf")
        heroAction = None
        if agentIndex == gameState.getNumAgents() - 1:
            nextAgent = 0
            nextDepth = depth - 1
        else:
            nextAgent, nextDepth = agentIndex + 1, depth
        for line in legalMoves:
            successorGameState = gameState.generateSuccessor(agentIndex, line)
            hero = self.agentAction(successorGameState, nextAgent, nextDepth)[0]
            if heroScore < hero:
                heroAction = line
                heroScore = hero
        return heroScore, heroAction

    def agentGhost(self, gameState, agentIndex, depth):
        if (gameState.isWin() or gameState.isLose() or depth == 0):
            return self.evaluationFunction(gameState), None
        legalMoves = gameState.getLegalActions(agentIndex)
        ghostScore = float('inf')
        ghostAction = None
        if agentIndex == gameState.getNumAgents() - 1:
            nextAgent = 0
            nextDepth =depth - 1
        else:
            nextAgent, nextDepth = agentIndex + 1, depth
        for line in legalMoves:
            successorGameState = gameState.generateSuccessor(agentIndex, line)
            ghost = self.agentAction(successorGameState, nextAgent, nextDepth)[0]
            if ghostScore > ghost:
                ghostAction = line
                ghostScore = ghost
        return ghostScore, ghostAction

    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.agentAction(gameState, 0, -float("inf"), float("inf"), self.depth)[1]

    def agentAction(self, gameState, agentIndex, alpha, beta, depth):
        # Hero
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, alpha, beta, depth)

        # Ghost
        else:
            return self.minValue(gameState, agentIndex, alpha, beta, depth)

    def maxValue(self, gameState, agentIndex, alpha, beta, depth):
        if (gameState.isWin() or gameState.isLose() or depth == 0):
            return self.evaluationFunction(gameState), None
        legalMoves = gameState.getLegalActions(agentIndex)
        currentScore = -float("inf")
        currentAction =  None
        if agentIndex != gameState.getNumAgents() - 1:
            maxAgent = agentIndex + 1
            maxDepth = depth
        else:
            maxAgent = 0
            maxDepth = depth - 1
        for line in legalMoves:
            successorGameState = gameState.generateSuccessor(agentIndex, line)
            maxScore = self.agentAction(successorGameState, maxAgent, alpha, beta, maxDepth)[0]
            if maxScore > currentScore: 
                currentScore = maxScore
                currentAction = line
            if maxScore > beta: return maxScore, line
            alpha = max(alpha, currentScore)
        return currentScore, currentAction

    def minValue(self, gameState, agentIndex, alpha, beta, depth):
        if (gameState.isWin() or gameState.isLose() or depth == 0):
            return self.evaluationFunction(gameState), None
        legalMoves = gameState.getLegalActions(agentIndex)
        currentScore = float("inf")
        currentAction = None

        if agentIndex != gameState.getNumAgents() - 1:
            minAgent = agentIndex + 1
            minDepth = depth
        else:
            minAgent = 0
            minDepth = depth - 1
            
        for line in legalMoves:
            successorGameState = gameState.generateSuccessor(agentIndex, line)
            minScore = self.agentAction(successorGameState, minAgent, alpha, beta, minDepth)[0]
            if minScore < currentScore: 
                currentScore = minScore
                currentAction = line
            if minScore < alpha: return minScore, line
            beta = min(beta, currentScore)
        return currentScore, currentAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # Hero
        if self.index == 0:
            return self.expectAction(gameState, self.index, self.depth + 1)[1]
        
        # Ghost
        else:
            return random.choice(gameState.getLegalActions(self.index))
    
    def expectAction(self, gameState, agentIndex, depth):
            if (agentIndex == 0):
                nextDepth = depth - 1
            else:
                nextDepth = depth
            if (gameState.isWin() or gameState.isLose() or nextDepth == 0):
                return self.evaluationFunction(gameState), None

            legalMoves = gameState.getLegalActions(agentIndex)
            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            expectedValue = 0.0
            heroValue = -float("inf")
            heroAction = None

            # Hero
            if agentIndex == 0:
                for line in legalMoves:
                    expectedValue = self.expectAction(gameState.generateSuccessor(agentIndex, line), nextAgent, nextDepth)[0]
                    if expectedValue > heroValue:
                        heroValue = expectedValue
                        heroAction = line
                return heroValue, heroAction

            # Ghost
            else :
                for line in legalMoves:
                    expectedValue += self.expectAction(gameState.generateSuccessor(agentIndex, line), nextAgent, nextDepth)[0]
                return expectedValue / len(legalMoves), None
        


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: My unstoppable evaluation function takes a extreme bias to kill ghosts when empowered with the pellet 
    while consuming as much as food as possible. By taking into consideration the nearest food, nearest ghost, and the 
    scared timer of a ghost, take the Manhattan Distance to the nearest ghost and nearest food. Yields higher evaluation
    score when ghosts are far and food is close, and yields lower evaluation score when non-scared ghosts are near and
    food is far.
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    nearestFood = float('inf')
    nearestGhost = float('inf')
    foodList = newFood.asList()

    if not foodList:
            nearestFood = 0
    for food in foodList:
        nearestFood = min(nearestFood, manhattanDistance(food, newPos))

    for ghost in newGhostStates:
        ghostX, ghostY = ghost.getPosition()
        if ghost.scaredTimer == 0: 
            nearestGhost = min(nearestGhost, manhattanDistance((ghostX, ghostY), newPos))

    hero = (currentGameState.getScore() - 5 / (nearestGhost + 1)) - (nearestFood / 2)
    return hero

# Abbreviation
better = betterEvaluationFunction
