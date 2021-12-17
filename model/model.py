import numpy as np
import matplotlib.pyplot as plt
import random

class Q_module:
	def __init__(self):
		self.state = {}
		self.actions = []
		self.q_table= {}
		self.reward_history = []

	def updateActions(self, tasks):
		for task in tasks:
			vals = []
			count = task.currentCount
			vals.append(count*task.period + task.phase)
			vals.append(count*task.deadline)
			vals.append(task.ID)
			vals.append(task.exec_time)
			vals.append(count)
			vals.append(task.period)
			a = Action(vals)
			self.actions.append(a)


	def calcReward(self, t, curr_action, action_obj, action):
		if curr_action == -1:
			#Initlially return a reward of 1 since there are no preemtions
			return 1

		if t > action_obj.deadline:
			# If the deadline is missed, penalize by 50
			return -10000

		if action_obj.execution > 0 and action != 0:
			# If preemption, penalize by 1
			return -1

		return 1 #Return a positive reward if current action is not preempted



	def train(self, hyperperiod, n=300, alpha=0.1, gamma=0.6, epsilon=0.3):
		for i in range(n):

			epochs, total_reward = 0, 0
			t = -1
			curr_action = -1
			total_reward = 0
			# print(len(self.actions))

			while t <= hyperperiod:

				if curr_action != -1 and curr_action != 0:
					action_obj.execution -= 1

				if t != -1:
					if action_obj.execution <= 0 :
						action_obj.count += 1
						action_obj.start = action_obj.count*action_obj.period

					self.actions.append(action_obj)

				if random.uniform(0, 1) <= epsilon:
					# Explore other actions
					rand_idx = random.randint(0, len(self.actions))
					if rand_idx == len(self.actions):
						action = 0
					else:	
						action_obj = self.actions[rand_idx]
						action = action_obj.ID
				else:
					# Exploit: Pick the action with highest reward
					max_reward = 0
					max_action = 0
					for key in self.q_table:
						if key[0] == t and key[1] == curr_action:
							if self.q_table[key] > max_reward:
								max_reward = self.q_table[key]
								max_action = key[2]

					if max_action == len(self.actions):
						action = 0
					else:
						action_obj = self.actions[max_action]
						action = action_obj.ID

				if action_obj.execution<=0:
					self.actions.remove(action_obj)
					continue

				next_state = (t+1, action)
				reward = self.calcReward(t, curr_action, action_obj, action)

				if (t, curr_action, action) in self.q_table:
					old_value = self.q_table[(t, curr_action, action)]
				else:
					self.q_table[(t, curr_action, action)] = 0
					old_value = 0

				next_max = 0
				for key in self.q_table:
					if key[0] == t+1 and key[1] == action:
						if self.q_table[key] > next_max:
							next_max = self.q_table[key]

				new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
				self.q_table[(t, curr_action, action)] = new_value

				t += 1
				curr_action = action
				total_reward += reward

				epochs += 1

			# print(i)
			if (i % 5 == 0):
				print(i)

			self.reward_history.append(total_reward)

	def visualizeReward(self):
		x_values = [i for i in range(1000)]
		print(len(self.reward_history), len(x_values))
		plt.plot(x_values, self.reward_history)
		plt.title("Total reward vs iteration")
		plt.xlabel("iteration")
		plt.ylabel("Total Reward")

		plt.show()



class Action:
	def __init__(self, vals):
		self.start = vals[0]
		self.deadline = vals[1]
		self.ID = vals[2]
		self.execution = vals[3]
		self.const_exec	= vals[3]
		self.count = vals[4]
		self.period = vals[5]
