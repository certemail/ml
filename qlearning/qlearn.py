#!/usr/bin/env python
import random
import argparse
import logging

#---global variables-----------------------------------------------------------
# grid dimensions
NUM_ROWS = 15 
NUM_COLS = 15 

# learning parameters
GAMMA = 0.9
LEARNING_RATE = 0.5

# exploration probability
EPSILON = 0.10

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
    logging.info("initializing grid...")
    grid_world = [[0.0 for col in range(NUM_COLS)] for row in range(NUM_ROWS)]
    logging.info("exit position:    " + "(" + str(END_STATE_ROW) + "," + str(END_STATE_COL) + ")")
    logging.info("penalty position: " + "(" + str(PENALTY_ROW) + "," + str(PENALTY_COL) + ")")
    grid_world[PENALTY_ROW][PENALTY_COL] = REWARD_IN_PENALTY_SQUARE
    grid_world[END_STATE_ROW][END_STATE_COL] = REWARD_ON_EXIT
    return grid_world

def initialize_q_table():
    NUM_ROWS_IN_Q_TABLE = (NUM_ROWS * NUM_ROWS) - 1
    logging.info("initializing q table...")
    logging.info("number of rows in q-table: " + str(NUM_ROWS_IN_Q_TABLE))
    q_table = [[0.0 for col in range(NUM_POSSIBLE_ACTIONS)] for row in range(NUM_ROWS_IN_Q_TABLE)]
    return q_table

def display_grid(grid_world):
    for row in grid_world:
        logging.debug(row)
    logging.debug("------------")
#---display_grid---------------------------------------------------------------

def display_q_table(q_table):
    # show q_table, rounded to 3 decimal places
    state_number = 0
    logging.debug('\t            {}      {}      {}      {}'.format('UP', 'DOWN', 'LEFT', 'RIGHT'))
    for row in q_table:
        rounded_row = [ '%.3f' % elem for elem in row]
        logging.debug('state {}: {} --> max-q: {:.3f}'.format(state_number, rounded_row, max(row)))
        state_number += 1
    logging.debug("------------")
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
    logging.debug("choose_action()...")
    # exploration (do completely random action)
    rand = random.random()
    if rand < EPSILON:
        logging.debug("RANDOM ACTION SELECTED!!" + str(rand))
        return random.choice(POSSIBLE_ACTIONS)

    x,y = convert_current_state_to_coordinates(current_state)
    logging.debug('\tq-values for current state {} ({},{}) are: {}'.format(current_state, x, y, q_table[current_state])) 

    # get max q-value for the current state
    max_q_value = max(q_table[current_state])
    count = q_table[current_state].count(max_q_value)
    logging.debug('\tmax q-value: {} appears {} times'.format(max_q_value, count))

    # if max_q_value exists for more than one action, randomly select an action
    if count > 1:
        logging.debug('\tneed to choose random action with max q-value')
        indices_with_max_q_value = [i for i in range(NUM_POSSIBLE_ACTIONS) if q_table[current_state][i] == max_q_value]
        logging.debug('\tindicies that have max_q_value: {}'.format(indices_with_max_q_value))
        idx = random.choice(indices_with_max_q_value)
        action = POSSIBLE_ACTIONS[idx]
        logging.debug('\trandom action selected from max q value: {}'.format(action))
        return action
    else:
        # get index of max_q_value
        idx = q_table[current_state].index(max_q_value)
        action = POSSIBLE_ACTIONS[idx]        
        return action
#---choose_action--------------------------------------------------------------

def get_next_state(current_state, action):
#returns the next state (grid cell) after moving
    logging.debug("get_next_state()...")
    x,y = convert_current_state_to_coordinates(current_state)

    # move UP
    if action == 'UP':
        logging.debug('\tchecking moving up:    ({},{})'.format(x-1, y))
        if x-1 < 0:
            logging.debug("\t\tin top row, can't move up! staying in same cell...")
            return(current_state)
        else:
            return(convert_coordinates_to_current_state(x-1, y))

    # move DOWN
    elif action == 'DOWN':    
        logging.debug('\tchecking moving down:  ({},{})'.format(x+1, y))
        if x+1 > NUM_ROWS -1:
            logging.debug("\t\tin last row, can't move down! staying in same cell...")
            return(current_state)
        else:
            return(convert_coordinates_to_current_state(x+1, y))

    # move LEFT
    elif action == 'LEFT':
        logging.debug('\tchecking moving left:  ({},{})'.format(x, y-1))
        if y-1 < 0:
            logging.debug("\t\tin left-most column, can't move left! staying in same cell...")
            return(current_state)
        else:
            return(convert_coordinates_to_current_state(x, y-1))

    # move RIGHT
    elif action == 'RIGHT':
        logging.debug('\tchecking moving right: ({},{})'.format(x, y+1))
        if y+1 > NUM_COLS-1:
            logging.debug("\t\tin right-most column, can't move right! staying same cell...")
            return(current_state)
        else:
            return(convert_coordinates_to_current_state(x, y+1))
#---get_next_state-------------------------------------------------------------

def compute_immediate_reward_and_update_q_table(previous_state, action_taken, new_state):
    global GOAL_STATE_VALUE
    logging.debug("compute_immediate_reward_and_update_q_table()...")
    logging.debug('\tprevious state: {}, action taken: {}, new state: {}'.format(previous_state, action_taken, new_state))

    # reached the terminal state
    if new_state == GOAL_STATE:
        logging.debug("\tnew_state is goal_state!")
        act_action_idx = POSSIBLE_ACTIONS.index(action_taken)
        logging.debug('\tindex into q entry for {} is: {}'.format(action_taken, act_action_idx))
        previous_state_q_value_for_action_just_taken = q_table[previous_state][act_action_idx]
        logging.debug('\tprevious_state_q_value_for_action_just_taken is: {}'.format(previous_state_q_value_for_action_just_taken))

        # compute new q-value (using GOAL_STATE_VALUE as 'q_value' for terminal state)
        new_q_value_for_previous_state = previous_state_q_value_for_action_just_taken + \
            (LEARNING_RATE * (REWARD_FOR_MAKING_ANY_MOVE + (GAMMA * GOAL_STATE_VALUE) - previous_state_q_value_for_action_just_taken))
        
        logging.debug('updated q-value {}'.format(new_q_value_for_previous_state))

        # update q-table for previous state for the action just taken
        q_table[previous_state][act_action_idx] = new_q_value_for_previous_state

        # TODO update utility value for goal state (is this correct?)
        GOAL_STATE_VALUE = REWARD_ON_EXIT
        logging.debug('updated utility value for goal state is: {}'.format(GOAL_STATE_VALUE))

    # regular update (terminal state not reached)
    else:
        logging.debug('\tq entry for new state {} is: {}'.format(new_state, q_table[new_state]))
        max_q_of_new_state = max(q_table[new_state])

        act_action_idx = POSSIBLE_ACTIONS.index(action_taken)
        logging.debug('\tindex into q entry for {} is: {}'.format(action_taken, act_action_idx))
        previous_state_q_value_for_action_just_taken = q_table[previous_state][act_action_idx]
        logging.debug('\tprevious_state_q_value_for_action_just_taken is: {}'.format(previous_state_q_value_for_action_just_taken))

        # compute new q-value
        new_q_value_for_previous_state = previous_state_q_value_for_action_just_taken + \
            (LEARNING_RATE * (REWARD_FOR_MAKING_ANY_MOVE + (GAMMA * max_q_of_new_state) - previous_state_q_value_for_action_just_taken))

        logging.debug('updated q-value {}'.format(new_q_value_for_previous_state))

        # update q-table for previous state for the action just taken
        q_table[previous_state][act_action_idx] = new_q_value_for_previous_state
#---compute_immediate_reward_and_update_q_table--------------------------------

def calculate_optimal_policy(q_table):
    print("calculating optimal policy...")

    # show q_table, rounded to 3 decimal places
    logging.info('final q_table:')
    logging.info("------------")
    state_number = 0
    logging.info('\t          {}      {}      {}      {}'.format('UP', 'DOWN', 'LEFT', 'RIGHT'))
    for row in q_table:
        rounded_row = [ '%.3f' % elem for elem in row]
        logging.info('state {}: {} --> max-q: {:.3f}'.format(state_number, rounded_row, max(row)))
        state_number += 1
    logging.info("------------")

    optimal_path = []
    start_state = 0

    current_state = start_state
    while current_state != GOAL_STATE:
        optimal_path.append(current_state)
        row = q_table[current_state]
        max_q = max(row)
        idx = row.index(max_q)
        direction = POSSIBLE_ACTIONS[idx]

        next_state = get_next_state(current_state, direction) 
        current_state = next_state
    return optimal_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("num_episodes", help="number of episodes")
    parser.add_argument("--log_level", help="log level")
    args = parser.parse_args()

    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(filename='log.txt', filemode='w', level=numeric_level, format='%(levelname)s: %(message)s')

    num_episodes = int(args.num_episodes)

    # parameters for reducing epsilon 
    interval_to_reduce_epsilon = num_episodes * 0.10

    grid_world = initialize_grid()
    q_table = initialize_q_table()
    display_grid(grid_world) 
    display_q_table(q_table)

    print('Grid dimensions: {}x{}'.format(NUM_ROWS, NUM_COLS))
    print('Epsilon at {:.2f}'.format(EPSILON))
    print('Running {} episodes...'.format(num_episodes))

    for i in range(num_episodes):
        # start from beginning (upper left-hand corner at (0,0), reset after each episode and goal is reached)
        current_state = 0
        num_steps_until_goal_reached = 0

        while(current_state != GOAL_STATE):
            # observe current state
            row, col = convert_current_state_to_coordinates(current_state)
            logging.debug('current state: {} [position in grid: ({}, {})]'.format(current_state, row, col))

            # select an action 
            action = choose_action(current_state)
            logging.debug("action selected: " + action)

            # determine what the new state will be
            new_state = get_next_state(current_state, action)
            new_row, new_col = convert_current_state_to_coordinates(new_state) 
            logging.debug('moving to new state: {} ({},{}) '.format(new_state, new_row, new_col))
            # save current_state in order to update q-table
            previous_state = current_state

            # compute immediate reward and update the q-table entry for the current state
            compute_immediate_reward_and_update_q_table(previous_state, action, new_state)
            display_q_table(q_table)

            # move to the new state now 
            current_state = new_state

            num_steps_until_goal_reached += 1

        # decrease epsilon for exploration when num_episodes increases every ten percent
        if i % interval_to_reduce_epsilon == 0:
            EPSILON = EPSILON - .01
            #print('episode #{} took {} steps to reach goal state with epsilon now at {:.2f}'.format(i, num_steps_until_goal_reached, EPSILON))
            
        if i % 10 == 0:
            print('Episode #{}: epsilon at {:.2f}; steps to reach goal state: {}'.format(i, EPSILON, num_steps_until_goal_reached))
    
    path = calculate_optimal_policy(q_table)
    for state in path:
        print('state {} {}'.format(state, convert_current_state_to_coordinates(state)))
    print('GOAL  {} {}'.format(GOAL_STATE, convert_current_state_to_coordinates(GOAL_STATE)))
    

