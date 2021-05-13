import numpy as np
from collections import defaultdict

class QLearning:
    def __init__(self, actions):
        self.actions = actions
        self.alpha = 0.1  
        self.gamma = 0.9
        self.actions = actions
        self.epsilon = 0.01
        self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])

    def get_action(self, state):
        if np.random.uniform() > self.epsilon:
            action_values = self.q_table[state]
            argmax_actions = []  
            for i in range(len(action_values)):
                if action_values[i] == np.max(action_values):
                    argmax_actions.append(i)
            next_action = np.random.choice(argmax_actions)
        else:
            next_action = np.random.choice(self.actions)
        if self.epsilon > 0:
            self.epsilon -= 0.00001  
        if self.epsilon < 0:
            self.epsilon = 0

        return next_action

    def learn(self, current_state, current_action, reward, next_state):
        next_action = np.argmax(self.q_table[next_state])
        new_q = reward + self.gamma * self.q_table[next_state][int(next_action)]
        self.q_table[current_state][current_action] = (1 - self.alpha) * self.q_table[current_state][
            current_action] + self.alpha * new_q
