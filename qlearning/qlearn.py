#!/usr/bin/env python

#----------------------------------
NUM_POSSIBLE_ACTIONS = 4

# grid dimensions
NUM_ROWS = 5 
NUM_COLS = 5

# rewards
REWARD_ON_EXIT = 1.0
REWARD_IN_PENALTY_SQUARE = -1.0
REWARD_FOR_MAKING_ANY_MOVE = -0.04

# exit state position
END_STATE_ROW = NUM_ROWS - 1 
END_STATE_COL = NUM_COLS - 1 

# penalty position
PENALTY_ROW = END_STATE_ROW - 1 
PENALTY_COL = END_STATE_COL    

# number of episodes to train
NUM_EPISODES = 1
#----------------------------------

def display_grid(grid_world):
    for row in grid_world:
        print(row)
    #temp = grid_world
    #counter = 0
    #for i in range(NUM_ROWS):
    #    for j in range(NUM_COLS):
    #        temp[i][j] = counter
    #        counter += 1
    #    print(temp[i])
    print("------------")

def display_q_table(q_table):
    counter = 0
    for row in q_table:
        print("state " + str(counter) + ":" + str(row))
        counter += 1
    print("------------")

def convert_current_state_to_coordinates(current_state):
    row = current_state // NUM_ROWS
    col = current_state %  NUM_COLS
    return (row, col)

def convert_coordinates_to_current_state(row, col):
    return (row * NUM_ROWS + col)

def choose_action(current_state):
    print("choosing action...")
    x,y = convert_current_state_to_coordinates(current_state)
    print('available moves for: ({},{})'.format(x,y)) 

    # move up
    print('\tchecking moving up:    ({},{})'.format(x-1, y))
    if x-1 < 0:
        print("\t\tin top row, can't move up!")
        
    # move down
    print('\tchecking moving down:  ({},{})'.format(x+1, y))
    if x+1 > NUM_ROWS -1:
        print("\t\tin last row, can't move down!")

    # move left
    print('\tchecking moving left:  ({},{})'.format(x, y-1))
    if y-1 < 0:
        print("\t\tin left-most column, can't move left!")

    # move right
    print('\tchecking moving right: ({},{})'.format(x, y+1))
    if y+1 > NUM_COLS-1:
        print("\t\tin right-most column, can't move right!")

    pass

if __name__ == '__main__':
    # initialize grid
    print("initializing grid...")
    grid_world = [[0.0 for col in range(NUM_COLS)] for row in range(NUM_ROWS)]
    print("exit position:    " + "(" + str(END_STATE_ROW) + "," + str(END_STATE_COL) + ")")
    print("penalty position: " + "(" + str(PENALTY_ROW) + "," + str(PENALTY_COL) + ")")
    grid_world[PENALTY_ROW][PENALTY_COL] = REWARD_IN_PENALTY_SQUARE
    grid_world[END_STATE_ROW][END_STATE_COL] = REWARD_ON_EXIT
    display_grid(grid_world) 

    # initialize q-table
    NUM_ROWS_IN_Q_TABLE = (NUM_ROWS * NUM_ROWS) - 1
    print("initializing q table...")
    print("number of rows in q-table: " + str(NUM_ROWS_IN_Q_TABLE))
    q_table = [[0 for col in range(NUM_POSSIBLE_ACTIONS)] for row in range(NUM_ROWS_IN_Q_TABLE)]
    display_q_table(q_table)

    # initialize current state (upper left-hand corner at (0,0))
    current_state = 0 

    for i in range(NUM_EPISODES):

        # observe current state
        row, col = convert_current_state_to_coordinates(current_state)
        print('current state: {} [position in grid: ({}, {})]'.format(current_state, row, col))

        # select an action 
        choose_action(current_state)

        # execute action

        # receive immediate reward

        # update q_table
