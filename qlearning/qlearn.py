#!/usr/bin/env python
import random
import argparse

#---global variables-----------------------------------------------------------
# grid dimensions
NUM_ROWS = 5 
NUM_COLS = 5 

# learning parameters
GAMMA = 0.9
LEARNING_RATE = 0.5

# exploration probability
EPSILON = 0.01

# possible actions
NUM_POSSIBLE_ACTIONS = 4
POSSIBLE_ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

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

# initialize goal state (lower-right-hand corner)
GOAL_STATE = (NUM_ROWS * NUM_COLS) - 1
GOAL_STATE_VALUE = 0.0
#---global variables-----------------------------------------------------------

def initialize_grid():
    print("initializing grid...")
    grid_world = [[0.0 for col in range(NUM_COLS)] for row in range(NUM_ROWS)]
    print("exit position:    " + "(" + str(END_STATE_ROW) + "," + str(END_STATE_COL) + ")")
    print("penalty position: " + "(" + str(PENALTY_ROW) + "," + str(PENALTY_COL) + ")")
    grid_world[PENALTY_ROW][PENALTY_COL] = REWARD_IN_PENALTY_SQUARE
    grid_world[END_STATE_ROW][END_STATE_COL] = REWARD_ON_EXIT
    return grid_world

def initialize_q_table():
    NUM_ROWS_IN_Q_TABLE = (NUM_ROWS * NUM_ROWS) - 1
    print("initializing q table...")
    print("number of rows in q-table: " + str(NUM_ROWS_IN_Q_TABLE))
    q_table = [[0.0 for col in range(NUM_POSSIBLE_ACTIONS)] for row in range(NUM_ROWS_IN_Q_TABLE)]
    return q_table

def display_grid(grid_world):
    for row in grid_world:
        print(row)
    print("------------")
#---display_grid---------------------------------------------------------------

def display_q_table(q_table):
    # show q_table, rounded to 3 decimal places
    state_number = 0
    print('\t    {}      {}      {}      {}'.format('UP', 'DOWN', 'LEFT', 'RIGHT'))
    for row in q_table:
        rounded_row = [ '%.3f' % elem for elem in row]
        print('state {}: {} --> max-q: {:.3f}'.format(state_number, rounded_row, max(row)))
        state_number += 1
    print("------------")
#---display_q_table--------------------------------------------------------------

def convert_current_state_to_coordinates(current_state):
    row = current_state // NUM_ROWS
    col = current_state %  NUM_COLS
    return (row, col)
#---convert_current_state_to_coordinates----------------------------------------

def convert_coordinates_to_current_state(row, col):
    return (row * NUM_ROWS + col)
#---convert_coordinates_to_current_state---------------------------------------

def choose_action(current_state):
    print("choose_action()...")
    # exploration (do completely random action)
    rand = random.random()
    if rand < EPSILON:
        print("RANDOM ACTION SELECTED!!" + str(rand))
        return random.choice(POSSIBLE_ACTIONS)

    x,y = convert_current_state_to_coordinates(current_state)
    print('\tq-values for current state {} ({},{}) are: {}'.format(current_state, x, y, q_table[current_state])) 

    # get max q-value for the current state
    max_q_value = max(q_table[current_state])
    count = q_table[current_state].count(max_q_value)
    print('\tmax q-value: {} appears {} times'.format(max_q_value, count))

    # if max_q_value exists for more than one action, randomly select an action
    if count > 1:
        print('\tneed to choose random action with max q-value')
        indices_with_max_q_value = [i for i in range(NUM_POSSIBLE_ACTIONS) if q_table[current_state][i] == max_q_value]
        print('\tindicies that have max_q_value: {}'.format(indices_with_max_q_value))
        idx = random.choice(indices_with_max_q_value)
        action = POSSIBLE_ACTIONS[idx]
        print('\trandom action selected from max q value: {}'.format(action))
        return action
    else:
        # get index of max_q_value
        idx = q_table[current_state].index(max_q_value)
        action = POSSIBLE_ACTIONS[idx]        
        return action
#---choose_action--------------------------------------------------------------

def get_next_state(current_state, action):
#returns the next state (grid cell) after moving
    print("get_next_state()...")
    x,y = convert_current_state_to_coordinates(current_state)

    # move UP
    if action == 'UP':
        print('\tchecking moving up:    ({},{})'.format(x-1, y))
        if x-1 < 0:
            print("\t\tin top row, can't move up! staying in same cell...")
            return(current_state)
        else:
            return(convert_coordinates_to_current_state(x-1, y))

    # move DOWN
    elif action == 'DOWN':    
        print('\tchecking moving down:  ({},{})'.format(x+1, y))
        if x+1 > NUM_ROWS -1:
            print("\t\tin last row, can't move down! staying in same cell...")
            return(current_state)
        else:
            return(convert_coordinates_to_current_state(x+1, y))

    # move LEFT
    elif action == 'LEFT':
        print('\tchecking moving left:  ({},{})'.format(x, y-1))
        if y-1 < 0:
            print("\t\tin left-most column, can't move left! staying in same cell...")
            return(current_state)
        else:
            return(convert_coordinates_to_current_state(x, y-1))

    # move RIGHT
    elif action == 'RIGHT':
        print('\tchecking moving right: ({},{})'.format(x, y+1))
        if y+1 > NUM_COLS-1:
            print("\t\tin right-most column, can't move right! staying same cell...")
            return(current_state)
        else:
            return(convert_coordinates_to_current_state(x, y+1))
#---get_next_state-------------------------------------------------------------


def compute_immediate_reward_and_update_q_table(previous_state, action_taken, new_state):
    global GOAL_STATE_VALUE
    print("compute_immediate_reward_and_update_q_table()...")
    print('\tprevious state: {}, action taken: {}, new state: {}'.format(previous_state, action_taken, new_state))

    # reached the terminal state
    if new_state == GOAL_STATE:
        print("\tnew_state is goal_state!")
        act_action_idx = POSSIBLE_ACTIONS.index(action_taken)
        print('\tindex into q entry for {} is: {}'.format(action_taken, act_action_idx))
        previous_state_q_value_for_action_just_taken = q_table[previous_state][act_action_idx]
        print('\tprevious_state_q_value_for_action_just_taken is: {}'.format(previous_state_q_value_for_action_just_taken))

        # compute new q-value (using GOAL_STATE_VALUE as 'q_value' for terminal state)
        new_q_value_for_previous_state = previous_state_q_value_for_action_just_taken + \
            (LEARNING_RATE * (REWARD_FOR_MAKING_ANY_MOVE + (GAMMA * GOAL_STATE_VALUE) - previous_state_q_value_for_action_just_taken))
        
        print('updated q-value {}'.format(new_q_value_for_previous_state))

        # update q-table for previous state for the action just taken
        q_table[previous_state][act_action_idx] = new_q_value_for_previous_state

        # TODO update utility value for goal state (is this correct?)
        GOAL_STATE_VALUE = REWARD_ON_EXIT
        print('updated utility value for goal state is: {}'.format(GOAL_STATE_VALUE))

    # regular update (terminal state not reached)
    else:
        print('\tq entry for new state {} is: {}'.format(new_state, q_table[new_state]))
        max_q_of_new_state = max(q_table[new_state])

        act_action_idx = POSSIBLE_ACTIONS.index(action_taken)
        print('\tindex into q entry for {} is: {}'.format(action_taken, act_action_idx))
        previous_state_q_value_for_action_just_taken = q_table[previous_state][act_action_idx]
        print('\tprevious_state_q_value_for_action_just_taken is: {}'.format(previous_state_q_value_for_action_just_taken))

        # compute new q-value
        new_q_value_for_previous_state = previous_state_q_value_for_action_just_taken + \
            (LEARNING_RATE * (REWARD_FOR_MAKING_ANY_MOVE + (GAMMA * max_q_of_new_state) - previous_state_q_value_for_action_just_taken))

        print('updated q-value {}'.format(new_q_value_for_previous_state))

        # update q-table for previous state for the action just taken
        q_table[previous_state][act_action_idx] = new_q_value_for_previous_state
#---compute_immediate_reward_and_update_q_table--------------------------------


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("num_episodes", help="number of episodes")
    args = parser.parse_args()

    num_episodes = int(args.num_episodes)

    grid_world = initialize_grid()
    q_table = initialize_q_table()
    display_grid(grid_world) 
    display_q_table(q_table)

    print('running {} episodes'.format(num_episodes))
    for i in range(num_episodes):
        # start from beginning (upper left-hand corner at (0,0), reset after each episode and goal is reached)
        current_state = 0
        num_steps_until_goal_reached = 0

        # TODO decrease epsilon every 1000 episodes

        while(current_state != GOAL_STATE):
            # observe current state
            row, col = convert_current_state_to_coordinates(current_state)
            print('current state: {} [position in grid: ({}, {})]'.format(current_state, row, col))

            # select an action 
            action = choose_action(current_state)
            print("action selected: " + action)

            # determine what the new state will be
            new_state = get_next_state(current_state, action)
            new_row, new_col = convert_current_state_to_coordinates(new_state) 
            print('moving to new state: {} ({},{}) '.format(new_state, new_row, new_col))
            # save current_state in order to update q-table
            previous_state = current_state

            # compute immediate reward and update the q-table entry for the current state
            compute_immediate_reward_and_update_q_table(previous_state, action, new_state)
            display_q_table(q_table)

            # move to the new state now 
            current_state = new_state

            num_steps_until_goal_reached += 1

        print('episode #{} took {} steps to reach goal state'.format(i, num_steps_until_goal_reached))
