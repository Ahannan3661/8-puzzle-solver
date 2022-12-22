from copy import deepcopy
import numpy as np
import time


# takes the input of current states and evaluvates the best path to goal state
def bestsolution(state): 
    #ME changed 9->16
    bestsol = np.array([], int).reshape(-1, 16)
    count = len(state) - 1
    while count != -1:
        bestsol = np.insert(bestsol, 0, state[count]['puzzle'], 0)
        count = (state[count]['parent'])
         #ME changed 3,3->4,4
    return bestsol.reshape(-1, 4, 4)


# this function checks for the uniqueness of the iteration(it) state, weather it has been previously traversed or not.
def all(checkarray):
    set = []
    for it in set:
        for checkarray in it:
            return 1
        else:
            return 0


def heuristic(puzzle, goal):
    #ME changed 3->4
    a = abs(puzzle // 4 - goal // 4)
    b = abs(puzzle % 4 - goal % 4)
    mhcost = a + b
    return sum(mhcost[1:])


# will indentify the coordinates of each of goal or initial state values
def coordinates(puzzle):
    #ME changed 9->16
    pos = np.array(range(16))
    for p, q in enumerate(puzzle):
        pos[q] = p
    return pos


def evaluate(puzzle, goal):
    #Me changed steps to perform on a 4x4 grid
    steps = np.array([('up', [0, 1, 2, 3], -4), ('down', [12, 13, 14,15], 4), ('left', [0, 4, 8,12], -1), ('right', [3, 7, 11,15], 1)],
                     dtype=[('move', str, 1), ('position', list), ('head', int)])
    #print(steps)
    dtstate = [('puzzle', list), ('parent', int), ('gn', int), ('hn', int)]

    costg = coordinates(goal)
    parent = -1
    gn = 0
    hn = heuristic(coordinates(puzzle), costg)
    state = np.array([(puzzle, parent, gn, hn)], dtstate)

    # We make use of priority queues with position as keys and fn as value.
    dtpriority = [('position', int), ('fn', int)]
    priority = np.array([(0, hn)], dtpriority)
    #ME program didn't stop when start_time was in while loop so i moved it out and now it does stop
    start_time = time.time()
    while 1:
        #print(priority)
        priority = np.sort(priority, kind='mergesort', order=['fn', 'position'])
        #print(priority)
        position, fn = priority[0]
        
        priority = np.delete(priority, 0, 0)
        # sort priority queue using merge sort,the first element is picked for exploring remove from queue what we are exploring
        puzzle, parent, gn, hn = state[position]
        puzzle = np.array(puzzle)
        # Identify the blank square in input
        #ME instead of one blank now we have two so i made a list that contains both the blanks 
        blanks = {int(np.where(puzzle == 0)[0]),int(np.where(puzzle == 1)[0])}
        gn = gn + 1
        c = 1
        
        for s in steps:
            c = c + 1
            #ME added this loop to check both blanks and pick the best move
            for blank in blanks:
                if blank not in s['position']:
                    # generate new state as copy of current
                    openstates = deepcopy(puzzle)
                    #print(s['head'])
                    openstates[blank], openstates[blank + s['head']] = openstates[blank + s['head']], openstates[blank]
                    # The all function is called, if the node has been previously explored or not
                    if ~(np.all(list(state['puzzle']) == openstates, 1)).any():
                        end_time = time.time()
                        if ((end_time - start_time) > 90):
                               print(" The 8 puzzle is unsolvable ! \n")
                               exit

                        hn = heuristic(coordinates(openstates), costg)
                        # generate and add new state in the list
                        q = np.array([(openstates, position, gn, hn)], dtstate)
                        state = np.append(state, q, 0)
                        # f(n) is the sum of cost to reach node and the cost to rech fromt he node to the goal state
                        fn = gn + hn

                        q = np.array([(len(state) - 1, fn)], dtpriority)
                        priority = np.append(priority, q, 0)
                        # Checking if the node in openstates are matching the goal state.
                        if np.array_equal(openstates, goal):
                            return state, len(priority)

    return state, len(priority)


def solve(puzzle, goal):
    state, visited = evaluate(puzzle, goal) 
    bestpath = bestsolution(state)
    #print(str(bestpath).replace('[', ' ').replace(']', '')) 
    totalmoves = len(bestpath) - 1
    #print('Steps to reach goal:',totalmoves)
    visit = len(state) - visited
    #print('Total nodes visited: ',visit, "\n") 
    #print('Total generated:', len(state)) 
    return totalmoves, visit, len(state)

puzzle =[ 
    2,  3,  4,   5,
    6,  7,  8,   9,
    10, 0, 12, 13,
    14, 15,  11, 1
]

goal = [
    2,  3,  4,   5,
    6,  7,  8,   9,
    10, 11, 12,  13,
    14, 15, 0,   1
]

print(solve(puzzle, goal))
