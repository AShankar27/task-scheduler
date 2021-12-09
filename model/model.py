import numpy as np
import matplotlib.pyplot as plt

class Q_module:
	def __init__(self):
		self.state = {}
		self.actions = [0]
		self.q_table= {}
		self.reward_history = []

	def updateActions(self, tasks):
		for task in tasks:
			count = task.currentCount
			start_time = count*task.period + task.phase
			deadline = count*task.deadline

	def calcReward(self, t, curr_action, action):
		if curr_action == -1:
			#Initlially return a reward of 1 since there are no preemtions
			return 1

		if t > curr_action.deadline:
			# If the deadline is missed, penalize by 50
			return -10000

		if curr_action.execution > 0 and action != 0:
			# If preemption, penalize by 1
			return -1

		return 1 #Return a positive reward if current action is not preempted



	def train(self, hyperperiod, alpha=0.1, gamma=0.6, epsilon=0.3):
		for i in range(10000):

			epochs, total_reward = 0, 0
			t = -1
			curr_action = -1
			total_reward = 0

			while t <= hyperperiod:

				if curr_action != -1:
					curr_action.execution -= 1

				if random.uniform(0, 1) <= epsilon:
					# Explore other actions
					rand_idx = random.randint(0, len(self.actions))
					action = self.actions[rand_idx]
				else:
					# Exploit: Pick the action with highest reward
					action = self.actions[]

				next_state = (t+1, action)
				reward = self.calcReward(t, curr_action, action)

				if (t, curr_action, action) in q_table:
					old_value = q_table[(t, curr_action, action)]
				else:
					q_table[(t, curr_action, action)] = 0
					old_value = 0

				next_max = 0
				for key in q_table:
					if key[0] == t and key[1] == action:
						if q_table[key] > next_max:
							next_max = q_table[key]

				new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
				q_table[(t, curr_action, action)] = new_value

				t += 1
				curr_action = action
				total_reward += reward

				epochs += 1

			self.reward_history[i] = total_reward

	def visualizeReward(self):
		x_values = [i for i in range(10000)]
		plt.plot(x_values, self.reward_history)
		plt.title("Total reward vs iteration")
		plt.xlable("iteration")
		plt.ylabel("Reward")

		plt.show()



class Action:
	def __init__(self, vals):
		self.start = vals[0]
		self.deadline = vals[1]
		self.ID = vals[2]
		self.execution = vals[3]
