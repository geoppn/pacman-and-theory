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
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # INITIALIZE VARIABLES
        foodList = newFood.asList()
        if foodList:
            # CALCULATE THE MINIMUM DISTANCE TO THE NEAREST FOOD
            minFoodDistance = min([manhattanDistance(newPos, food) for food in foodList])
        else:
            minFoodDistance = 1  # A SMALL VALUE TO AVOID DIVISION BY ZERO

        # CALCULATE THE DISTANCE TO THE NEAREST NON-SCARED GHOST
        ghostDistances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        minGhostDistance = min(ghostDistances) if ghostDistances else 1

        # CHECK IF ANY GHOST IS TOO CLOSE AND NOT SCARED
        scared = any([scaredTime > 0 for scaredTime in newScaredTimes])
        if minGhostDistance <= 1 and not scared:
            ghostScore = -float('inf')  # VERY BAD SCORE IF GHOST IS TOO CLOSE
        else:
            ghostScore = 1.0 / minGhostDistance

        # CALCULATE THE FINAL SCORE WITH WEIGHTS FOR FOOD AND GHOSTS
        score = successorGameState.getScore() + (1.0 / minFoodDistance) + ghostScore

        return score

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
    YOUR MINIMAX AGENT (QUESTION 2)
    """

    def getAction(self, gameState: GameState):
        """
        RETURNS THE MINIMAX ACTION FROM THE CURRENT GAMESTATE USING SELF.DEPTH AND SELF.EVALUATIONFUNCTION.
        """
        # GET LEGAL ACTIONS FOR PACMAN
        legalActions = gameState.getLegalActions(0)
        bestScore = -float('inf')
        bestAction = None

        # EVALUATE EACH ACTION USING MINIMAX
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            score = self.minValue(successor, 0, 1)
            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction

    def maxValue(self, state, depth):
        # TERMINAL STATE OR MAX DEPTH REACHED
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        v = -float('inf')
        legalActions = state.getLegalActions(0)
        if not legalActions:
            return self.evaluationFunction(state)
        # EVALUATE SUCCESSOR STATES FOR PACMAN
        for action in legalActions:
            successor = state.generateSuccessor(0, action)
            v = max(v, self.minValue(successor, depth, 1))
        return v

    def minValue(self, state, depth, agentIndex):
        # TERMINAL STATE REACHED
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        v = float('inf')
        legalActions = state.getLegalActions(agentIndex)
        if not legalActions:
            return self.evaluationFunction(state)
        numAgents = state.getNumAgents()
        # EVALUATE SUCCESSOR STATES FOR GHOSTS
        for action in legalActions:
            successor = state.generateSuccessor(agentIndex, action)
            if agentIndex == numAgents - 1:
                # LAST GHOST; NEXT AGENT IS PACMAN, INCREMENT DEPTH
                v = min(v, self.maxValue(successor, depth + 1))
            else:
                # NEXT GHOST
                v = min(v, self.minValue(successor, depth, agentIndex + 1))
        return v
    
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    YOUR MINIMAX AGENT WITH ALPHA-BETA PRUNING (QUESTION 3)
    """

    def getAction(self, gameState: GameState):
        """
        RETURNS THE MINIMAX ACTION USING SELF.DEPTH AND SELF.EVALUATIONFUNCTION
        """
        # DEFINE ALPHA-BETA FUNCTION INSIDE GETACTION
        def alphaBeta(state, depth, agentIndex, alpha, beta):
            # CHECK IF STATE IS WIN, LOSE, OR MAX DEPTH REACHED
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # GET LEGAL ACTIONS FOR CURRENT AGENT
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state)
            # PACMAN'S TURN (MAXIMIZER)
            if agentIndex == 0:
                v = -float('inf')
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    v = max(v, alphaBeta(successor, depth, agentIndex + 1, alpha, beta))
                    if v > beta:
                        return v  # PRUNE
                    alpha = max(alpha, v)
                return v
            else:
                # GHOSTS' TURN (MINIMIZER)
                v = float('inf')
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    nextAgent = agentIndex + 1
                    nextDepth = depth
                    if nextAgent == state.getNumAgents():
                        nextAgent = 0  # BACK TO PACMAN
                        nextDepth += 1  # INCREMENT DEPTH
                    v = min(v, alphaBeta(successor, nextDepth, nextAgent, alpha, beta))
                    if v < alpha:
                        return v  # PRUNE
                    beta = min(beta, v)
                return v

        # INITIALIZE VARIABLES
        alpha = -float('inf')
        beta = float('inf')
        bestAction = None
        bestScore = -float('inf')

        # GET LEGAL ACTIONS FOR PACMAN
        legalActions = gameState.getLegalActions(0)
        if not legalActions:
            return None

        # EVALUATE EACH ACTION USING ALPHA-BETA PRUNING
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            score = alphaBeta(successor, 0, 1, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            if bestScore > beta:
                return bestAction  # PRUNE
            alpha = max(alpha, bestScore)

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        RETURNS THE EXPECTIMAX ACTION USING SELF.DEPTH AND SELF.EVALUATIONFUNCTION

        ALL GHOSTS SHOULD BE MODELED AS CHOOSING UNIFORMLY AT RANDOM FROM THEIR
        LEGAL MOVES.
        """
        # IMPLEMENT EXPECTIMAX SEARCH

        # DEFINE THE EXPECTIMAX FUNCTION
        def expectimax(state, depth, agentIndex):
            # CHECK FOR TERMINAL STATE OR MAX DEPTH REACHED
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # GET LEGAL ACTIONS FOR CURRENT AGENT
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state)

            # COMPUTE NEXT AGENT INDEX AND DEPTH
            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth + 1 if nextAgent == 0 else depth

            if agentIndex == 0:
                # PACMAN'S TURN (MAXIMIZER)
                maxValue = -float('inf')
                for action in legalActions:
                    # GENERATE SUCCESSOR STATE
                    successor = state.generateSuccessor(agentIndex, action)
                    # RECURSIVELY CALL EXPECTIMAX
                    value = expectimax(successor, nextDepth, nextAgent)
                    maxValue = max(maxValue, value)
                return maxValue
            else:
                # GHOSTS' TURN (EXPECTATION NODE)
                totalValue = 0
                for action in legalActions:
                    # GENERATE SUCCESSOR STATE
                    successor = state.generateSuccessor(agentIndex, action)
                    # RECURSIVELY CALL EXPECTIMAX
                    value = expectimax(successor, nextDepth, nextAgent)
                    totalValue += value
                # CALCULATE AVERAGE VALUE
                averageValue = totalValue / len(legalActions)
                return averageValue

        # FIND THE BEST ACTION FROM THE ROOT NODE
        bestScore = -float('inf')
        bestAction = None
        legalActions = gameState.getLegalActions(0)  # PACMAN'S LEGAL ACTIONS

        # ITERATE OVER LEGAL ACTIONS TO FIND THE BEST ONE
        for action in legalActions:
            # GENERATE SUCCESSOR STATE
            successor = gameState.generateSuccessor(0, action)
            # CALL EXPECTIMAX FOR THE SUCCESSOR STATE
            score = expectimax(successor, 0, 1)
            # UPDATE BEST SCORE AND BEST ACTION
            if score > bestScore:
                bestScore = score
                bestAction = action

        # RETURN THE BEST ACTION
        return bestAction

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    # GET PACMAN'S POSITION
    pacmanPos = currentGameState.getPacmanPosition()
    # GET FOOD POSITIONS
    food = currentGameState.getFood()
    foodList = food.asList()
    # GET GHOST STATES
    ghostStates = currentGameState.getGhostStates()
    # GET CAPSULE POSITIONS
    capsules = currentGameState.getCapsules()

    # INITIALIZE VARIABLES
    import sys
    closestFoodDist = sys.maxsize
    closestCapsuleDist = sys.maxsize
    scaredGhostScore = 0
    activeGhostPenalty = 0

    # CALCULATE DISTANCE TO THE CLOSEST FOOD
    if foodList:
        foodDistances = [manhattanDistance(pacmanPos, foodPos) for foodPos in foodList]
        closestFoodDist = min(foodDistances)
    else:
        closestFoodDist = 0

    # CALCULATE DISTANCES TO GHOSTS
    for ghostState in ghostStates:
        ghostPos = ghostState.getPosition()
        dist = manhattanDistance(pacmanPos, ghostPos)
        if ghostState.scaredTimer > 0:
            # SCARED GHOST
            if dist > 0:
                scaredGhostScore += 200 / dist
        else:
            # ACTIVE GHOST
            if dist <= 1:
                # TOO CLOSE TO A GHOST, AVOID
                return -float('inf')
            else:
                activeGhostPenalty += -2 / dist

    # CALCULATE DISTANCE TO THE CLOSEST CAPSULE
    if capsules:
        capsuleDistances = [manhattanDistance(pacmanPos, capsulePos) for capsulePos in capsules]
        closestCapsuleDist = min(capsuleDistances)
    else:
        closestCapsuleDist = 0

    # COMBINE THE FACTORS INTO A FINAL SCORE
    finalScore = score
    # SUBTRACT WEIGHTED DISTANCE TO THE CLOSEST FOOD
    finalScore += -1.5 * closestFoodDist
    # ADD SCARED GHOST SCORE
    finalScore += scaredGhostScore
    # ADD ACTIVE GHOST PENALTY
    finalScore += activeGhostPenalty
    # SUBTRACT WEIGHTED DISTANCE TO THE CLOSEST CAPSULE
    finalScore += -2 * closestCapsuleDist
    # SUBTRACT WEIGHTED NUMBER OF REMAINING FOOD
    finalScore += -10 * len(foodList)
    # SUBTRACT WEIGHTED NUMBER OF REMAINING CAPSULES
    finalScore += -20 * len(capsules)

    # RETURN THE FINAL SCORE
    return finalScore

# Abbreviation
better = betterEvaluationFunction
