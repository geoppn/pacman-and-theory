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
from game import Directions
from typing import List

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




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
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
    frontier = util.Stack() # STACK = PROJECT REQUIREMENT
    start_state = problem.getStartState() # GET THE STARTING STATE OF THE CURRENT PROBLEM
    frontier.push((start_state, []))  # STORE THE STARTING STATE AND AN EMPTY PATH [AVOIDING ERRORS]
    
    explored = set() # USE A SET TO STORE THE EXPLORED STATES
    
    while not frontier.isEmpty(): #MAIN DFS LOOP
        state, path = frontier.pop() # POP A NODE
        if problem.isGoalState(state): # IF THE STATE IS THE FOOD, RETURN THE APPROPRIATE PATH AS INSTRUCTED
            return path
        
        if state not in explored: # IF A STATE ISNT IN THE EXPLORED SET,
            explored.add(state) # ADD IT
            
            for successor, action, _ in problem.getSuccessors(state): # CHECK THE SUCCESSORS OF THE CURRENT STATE, IGNORE IF THEYRE EXPLORED
                if successor not in explored: # [AVOID EXPLORED STATES AS INSTRUCTED IN THE PROJECT]
                    new_path = path + [action] # ADD THE ACTION TO THE PATH
                    frontier.push((successor, new_path)) # GET THE NEW PATH INTO THE STACK
    
    # NO FEASIBLE SOLUTION
    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    frontier = util.Queue()
    start_state = problem.getStartState()
    frontier.push((start_state, []))  
    
    explored = set()
    
    while not frontier.isEmpty(): 
        state, path = frontier.pop()
        if problem.isGoalState(state):
            return path
        
        if state not in explored:
            explored.add(state)
            
            for successor, action, _ in problem.getSuccessors(state): # SAME CONCEPT SO FAR
                if successor not in explored and successor not in [s for s, _ in frontier.list]: # CHECK IF THE SUCCESSOR IS IN THE FRONTIER, QUEUE VERSION FOR BFS
                    new_path = path + [action]
                    frontier.push((successor, new_path))
    
    return []

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    frontier = util.PriorityQueue()
    start_state = problem.getStartState()
    frontier.push((start_state, []), 0)  # PRIORITY ADDED 
    
    currentcost = {start_state: 0} # DICTIONARY FOR COSTS
    
    while not frontier.isEmpty(): # SAME CONCEPT:
        state, path = frontier.pop()
        if problem.isGoalState(state):
            return path
        
        for successor, action, step_cost in problem.getSuccessors(state): # INCLUDE THE STEP COST
            new_cost = currentcost[state] + step_cost # ADD THE STEP COST TO THE CURRENT COST
            if successor not in currentcost or new_cost < currentcost[successor]: # IF THE SUCCESSOR ISNT IN THE CURRENT COST OR THE NEW COST IS LESS THAN THE CURRENT COST
                currentcost[successor] = new_cost # UPDATE THE COST ACCORDINGLY
                new_path = path + [action] 
                frontier.push((successor, new_path), new_cost)
    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    start_state = problem.getStartState()
    frontier.push((start_state, []), 0) 
    
    currentcost = {start_state: 0}
    
    while not frontier.isEmpty():
        state, path = frontier.pop()
        if problem.isGoalState(state):
            return path
        for successor, action, step_cost in problem.getSuccessors(state):
            new_cost = currentcost[state] + step_cost
            if successor not in currentcost or new_cost < currentcost[successor]:
                currentcost[successor] = new_cost
                priority = new_cost + heuristic(successor, problem) # ADD THE HEURISTIC TO THE PRIORITY
                new_path = path + [action]
                frontier.push((successor, new_path), priority)
    
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
