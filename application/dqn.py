from enum import *
import tensorflow as tf
import numpy as np

class DQN:
    def __init__(self, learning_rate, discount):
        self.learning_rate = learning_rate
        self.discount = discount  # How much we appreciate future reward over current

        # Input has 26 neurons. This 26 neurons represent state of the game!
        self.input_count = 26
        # Output is 49 neurons, each represents Q-value for action
        self.output_count = 49

        self.session = tf.compat.v1.Session()
        self.define_model()
        self.session.run(self.initializer)

    def define_model(self):
        # Input is an array of 26 items
        # Input is 2-dimensional, due to possibility of batched training data
        # NOTE: In this example we assume no batching.
        self.model_input = tf.compat.v1.placeholder(dtype=tf.float32, shape=[None, self.input_count])

        # Two hidden layers of 16 neurons with sigmoid activation initialized to zero for stability
        fc1 = tf.layers.dense(self.model_input, 32, activation=tf.sigmoid,
                              kernel_initializer=tf.constant_initializer(np.zeros((self.input_count, 32))))
        fc2 = tf.layers.dense(fc1, 40, activation=tf.sigmoid,
                              kernel_initializer=tf.constant_initializer(np.zeros((40, self.output_count))))

        # Output is 49 values, Q for all possible actions
        # Output is 2-dimensional, due to possibility of batched training data
        # NOTE: In this example we assume no batching.
        self.model_output = tf.layers.dense(fc2, self.output_count)

        # This is for feeding training output (a.k.a ideal target values)
        self.target_output = tf.compat.v1.placeholder(shape=[None, self.output_count], dtype=tf.float32)
        # Loss is mean squared difference between current output and ideal target values
        loss = tf.compat.v1.losses.mean_squared_error(self.target_output, self.model_output)
        # Optimizer adjusts weights to minimize loss, with the speed of learning_rate
        self.optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=self.learning_rate).minimize(loss)
        # Initializer to set weights to initial values
        self.initializer = tf.compat.v1.global_variables_initializer()

    def get_q_values(self, state):
        return self.session.run(self.model_output, feed_dict={self.model_input: state})[0]

    def train(self, old_state, action, reward, new_state):
        # Ask the model for the Q values of the old state (inference)
        old_state_q_values = self.get_q(old_state)

        # Ask the model for the Q values of the new state (inference)
        new_state_q_values = self.get_q(new_state)

        # Real Q value for the action we took. This is what we will train towards.
        old_state_q_values[action] = reward + self.discount * np.amax(new_state_q_values)

        # Setup training data
        training_input = self.to_one_hot(old_state)
        target_output = [old_state_q_values]
        training_data = {self.model_input: training_input, self.target_output: target_output}

        # Train
        self.session.run(self.optimizer, feed_dict=training_data)


class DQ:
    network = DQN(learning_rate=0.1, discount=0.95)
