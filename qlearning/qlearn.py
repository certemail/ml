#!/usr/bin/env python
import random
import argparse
import logging
from matplotlib import pyplot as plt

#---global variables-----------------------------------------------------------
# learning parameters
GAMMA = 0.9
LEARNING_RATE = 0.5

# exploration probability
EPSILON = 0.10

# possible actions
NUM_POSSIBLE_ACTIONS = 4
POSSIBLE_ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']
#---global variables-----------------------------------------------------------

def initialize_grid():
    logging.info("initializing grid...")
    end_state_row = NUM_ROWS - 1
    end_state_col = NUM_COLS - 1

    grid_world = [[0.0 for col in range(NUM_COLS)] for row in range(NUM_ROWS)]
    logging.info("exit position:    " + "(" + str(end_state_row) + "," + str(end_state_col) + ")")
    grid_world[end_state_row][end_state_col] = REWARD_ON_EXIT
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
        logging.debug('state {:4d}: {} --> max-q: {:.3f}'.format(state_number, rounded_row, max(row)))
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

def build_utility_matrix(q_table):
    print("Utility matrix:")
    utility_values = []
    for row in q_table:
        utility_values.append(max(row))
    utility_values.append(GOAL_STATE_VALUE)

    counter = 0
    for value in utility_values:
        print('{:+.3f}'.format(value), end=' ') 
        counter += 1
        if counter % NUM_COLS == 0:
            print()


def show_numbered_grid_states():
    state_num = 0
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            print('{:4d}'.format(state_num,i,j), end=' ')
            state_num += 1
        print() 

def show_graph(x_episodes, y_num_steps):
    logging.info('number of episodes:')
    logging.info(x_episodes)
    logging.info('number of steps:')
    logging.info(y_num_steps)
    
    title = 'Number of Steps to Reach Terminal State\n Reward per step: {}, Reward on exit: {}'.format(REWARD_FOR_MAKING_ANY_MOVE, REWARD_ON_EXIT)

    # plot graph of episodes vs. steps to reach goal
    plt.plot(x_episodes, y_num_steps)
    plt.title(title)
    plt.ylabel('Steps')
    plt.xlabel('Episodes')
    plt.show()

def show_optimal_policy(path):
    print('Optimal policy:') 
    for state in path:
        print('state {} {}'.format(state, convert_current_state_to_coordinates(state)))
    print('GOAL  {} {}'.format(GOAL_STATE, convert_current_state_to_coordinates(GOAL_STATE)))

def show_optimal_path(path):
    print('Optimal path:')
    state_num = 0
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            if state_num in path:
                print('{:4d}'.format(state_num), end=' ')
            elif state_num == GOAL_STATE:
                print('{:4d}'.format(GOAL_STATE), end=' ')
            else:
                print('{:>4}'.format('-'), end=' ')
            state_num += 1
        print() 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("num_rows", help="number of rows")
    parser.add_argument("num_cols", help="number of cols")
    parser.add_argument("num_episodes", help="number of episodes")
    parser.add_argument("reward_per_move", help="reward per move")
    parser.add_argument("reward_on_exit", help="reward on exit")
    parser.add_argument("--log", help="log level")
    args = parser.parse_args()

    if args.log:
        numeric_level = getattr(logging, args.log.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
        logging.basicConfig(filename='log.txt', filemode='w', level=numeric_level, format='%(levelname)s: %(message)s')

    global NUM_ROWS
    global NUM_COLS
    global GOAL_STATE
    global GOAL_STATE_VALUE
    global REWARD_FOR_MAKING_ANY_MOVE
    global REWARD_ON_EXIT

    num_episodes = int(args.num_episodes)
    NUM_ROWS = int(args.num_rows)
    NUM_COLS = int(args.num_cols)
    REWARD_FOR_MAKING_ANY_MOVE = float(args.reward_per_move)
    REWARD_ON_EXIT = float(args.reward_on_exit)

    GOAL_STATE = (NUM_ROWS * NUM_COLS) - 1
    GOAL_STATE_VALUE = 0.0

    # parameters for reducing epsilon 
    interval_to_reduce_epsilon = num_episodes * 0.10

    grid_world = initialize_grid()
    q_table = initialize_q_table()
    display_grid(grid_world) 
    display_q_table(q_table)

    print('Grid dimensions: {}x{}'.format(NUM_ROWS, NUM_COLS))
    print('Reward per move: {}'.format(REWARD_FOR_MAKING_ANY_MOVE))
    print('Reward on exit: {}'.format(REWARD_ON_EXIT))
    print('Epsilon at {:.2f}'.format(EPSILON))
    print('Running {} episodes...'.format(num_episodes))

    x_episodes = []
    y_num_steps = []

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

        # collect episode and number of steps for graphing
        x_episodes.append(i)
        y_num_steps.append(num_steps_until_goal_reached)

        # decrease epsilon for exploration when num_episodes increases every ten percent
        if i % interval_to_reduce_epsilon == 0:
            EPSILON = EPSILON - .01
            
        # display values every 10 episodes for number of steps it takes to reach the goal state and epsilon
        if i % 10 == 0:
            print('Episode {:4d} --> epsilon at {:.2f}; steps to reach goal state: {:4d}'.format(i, EPSILON, num_steps_until_goal_reached))

    print('{}'.format('='*25))
    print('Calculating optimal policy for {}x{} grid:'.format(NUM_ROWS, NUM_COLS))
    show_numbered_grid_states()
    print('{}'.format('='*25))

    path = calculate_optimal_policy(q_table)
    show_optimal_policy(path)
    
    print('{}'.format('='*25))
    show_optimal_path(path)

    print('{}'.format('='*25))
    build_utility_matrix(q_table)

    show_graph(x_episodes, y_num_steps)
