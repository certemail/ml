#!/usr/bin/env python

#----------------------------------
NUM_POSSIBLE_ACTIONS = 4

# grid dimensions
NUM_ROWS = 15 #3
NUM_COLS = 15 #4

# rewards
REWARD_ON_EXIT = 1.0
REWARD_IN_PENALTY_SQUARE = -1.0
REWARD_FOR_MAKING_ANY_MOVE = -0.04

# exit state position
END_STATE_ROW = NUM_ROWS - 1 #0
END_STATE_COL = NUM_COLS - 1 #3

# penalty position
PENALTY_ROW = END_STATE_ROW - 1 #1
PENALTY_COL = END_STATE_COL     #3

# number of episodes to train
NUM_EPISODES = 1
#----------------------------------

def display_grid(grid_world):
    for row in grid_world:
        print(row)

def display_q_table(q_table):
    for row in q_table:
        print(row)

def convert_current_state_to_coordinates(current_state):
    row = current_state // NUM_ROWS
    col = current_state %  NUM_COLS
    return row, col

def choose_action(current_state):
    pass

if __name__ == '__main__':
    print("starting grid world...")

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
        print('current position in grid: {}, {}'.format(row, col))

        # select an action 
        choose_action(current_state)

        # execute action

        # receive immediate reward

        # update q_table
