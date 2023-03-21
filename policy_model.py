import numpy as np
import pandas as pd
import csv
import random
import matplotlib.pyplot as plt
from datetime import datetime


def sarsa(input_csv, number_of_states, number_of_actions=3, input_discount=0.95, alpha=0.1):
    state_space = number_of_states
    action_space = number_of_actions
    # action value function
    Q = np.zeros((state_space, action_space))

    with open(input_csv, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for i, line in enumerate(reader):
            if i != 0:
                [temp] = line
                s, r, a, sp = temp.split(",")
                s, r, a, sp = int(s), int(r), int(a), int(sp)
                # Q[s, a] += α * (r + γ * (Q[s′,a']) - Q[s, a])
                Q[s-1, a-1] += alpha * (r + input_discount * Q[sp - 1, a - 1] - Q[s-1, a-1])

    policy = np.zeros(number_of_states)
    for i in range(number_of_states):
        flag_no_actions_rewards = True
        for j in Q[i]:
            if j != 0:
                flag_no_actions_rewards = False
        # there are some states in the medium and large problems that do not have
        # actions and rewards associated with them in the data provided
        if flag_no_actions_rewards:
            policy[i] = random.randint(0, number_of_actions - 1)
        else:
            policy[i] = np.argmax(Q[i])

    return policy


def q_learning_with_epsilon_greedy_exploration(input_csv, number_of_states, number_of_actions=3, input_discount=0.95, alpha=0.1, epsilon=0.2):
    state_space = number_of_states
    action_space = number_of_actions
    # action value function
    Q = np.zeros((state_space, action_space))

    with open(input_csv, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for i, line in enumerate(reader):
            if i != 0:
                [temp] = line
                s, r, a, sp = temp.split(",")
                s, r, a, sp = int(s), int(r), int(a), int(sp)
                # Q[s, a] += α * (r + γ * maximum(Q[s′,:]) - Q[s, a])
                max_val = np.max(Q[sp - 1])
                Q[s-1, a-1] += alpha * (r + input_discount * max_val - Q[s-1, a-1])

    policy = np.zeros(number_of_states)
    for i in range(number_of_states):
        flag_no_actions_rewards = True
        for j in Q[i]:
            if j != 0:
                flag_no_actions_rewards = False
        # there are some states in the medium and large problems that do not have
        # actions and rewards associated with them in the data provided
        if random.random() < epsilon:
            policy[i] = random.randint(0, number_of_actions - 1)
        else:
            if flag_no_actions_rewards:
                policy[i] = random.randint(0, number_of_actions - 1)
            else:
                policy[i] = np.argmax(Q[i])

    return policy


def q_learning(input_csv, number_of_states, number_of_actions=3, input_discount=0.95, alpha=0.1):
    state_space = number_of_states
    action_space = number_of_actions
    # action value function
    Q = np.zeros((state_space, action_space))

    with open(input_csv, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for i, line in enumerate(reader):
            if i != 0:
                [temp] = line
                s, r, a, sp = temp.split(",")
                s, r, a, sp = int(s), int(r), int(a), int(sp)
                # Q[s, a] += α * (r + γ * maximum(Q[s′,:]) - Q[s, a])
                max_val = np.max(Q[sp - 1])
                Q[s-1, a-1] += alpha * (r + input_discount * max_val - Q[s-1, a-1])

    policy = np.zeros(number_of_states)
    for i in range(number_of_states):
        flag_no_actions_rewards = True
        for j in Q[i]:
            if j != 0:
                flag_no_actions_rewards = False
        # policy[i] = random.randint(0, number_of_actions - 1)
        # there are some states in the medium and large problems that do not have
        # actions and rewards associated with them in the data provided
        if flag_no_actions_rewards:
            policy[i] = random.randint(0, number_of_actions - 1)
        else:
            policy[i] = np.argmax(Q[i])

    return policy


if __name__ == '__main__':
    # number_of_states = 6
    # small_q_learning = q_learning("small.csv", 6)
    #
    # with open('data/random_policy_small.policy', 'w') as f:
    #     for line in small_q_learning:
    #         f.write("%s\n" % str(int(line)))
    small_q_learning = q_learning("/data/small.csv", 6)

    with open('/data/small_q_learning.policy', 'w') as f:
        for line in small_q_learning:
            f.write("%s\n" % str(int(line)))

    small_sarsa_learning = sarsa("/data/small.csv", 6)

    with open('/data/small_sarsa_learning.policy', 'w') as f:
        for line in small_sarsa_learning:
            f.write("%s\n" % str(int(line)))
    # number_of_states = 52
    big_q_learning = q_learning("/data/big.csv", 52)

    with open('/data/big_q_learning.policy', 'w') as f:
        for line in big_q_learning:
            f.write("%s\n" % str(int(line)))

    big_sarsa_learning = sarsa("/data/big.csv", 52)

    with open('/data/big_sarsa_learning.policy', 'w') as f:
        for line in big_sarsa_learning:
            f.write("%s\n" % str(int(line)))