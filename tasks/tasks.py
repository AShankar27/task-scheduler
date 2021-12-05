import numpy as np
import re
from math import gcd

class TaskSet:
	def __init__(self):
		self.hyperperiod = 0
		self.frame_sizes = []
		self.tasks = []

	def updateTasks(self, filename):
		f = open(filename, 'r')
		lines = f.readlines()
		#self.tasks = np.zeros(shape = (len(lines), 4))
		for i, line in enumerate(lines):
			line_wb = re.sub(r"[()]", "", line)
			vals = np.fromstring(line_wb.strip(), dtype="float", sep=',')
			#print(vals)
			vals = np.round(vals, 1)
			t = Task(vals)
			self.tasks.append(t)

	def calculateHyperperiod(self):
		period = self.getPeriod()
		self.hyperperiod = np.lcm.reduce(np.array(period, dtype=int))

	def updateJobCount(self):
		for task in self.tasks:
			task.jobCount = int(self.hyperperiod/task.period)

	def getPeriod(self):
		period = []
		for task in self.tasks:
			period.append(task.period)

		return period

	def getDeadlines(self):
		deadlines = []
		for task in self.tasks:
			deadlines.append(task.deadline)

		return deadlines

	def getExecTimes(self):
		executionTime = []
		for task in self.tasks:
			executionTime.append(task.exec_time)

		return executionTime


	def getFrameSizes(self):
		self.calculateHyperperiod()
		exec_times = self.getExecTimes()
		deadlines = self.getDeadlines()
		frames = []
		maxC = int(max(exec_times))
		count = 0
		print(set(deadlines))

		for i in range(1, self.hyperperiod+1):
			if (self.hyperperiod % i == 0):
				frames.append(i)

		print(frames)
		for frame in frames:
			for deadline in set(deadlines):
				val = 2*frame - gcd(frame, int(deadline))
				if val <= deadline:
					count += 1
				else:
					break

			if (count == len(set(deadlines))):
				self.frame_sizes.append(frame)
			count = 0

		return self.frame_sizes


class Task:
	def __init__(self, values):
		self.phase = values[0]
		self.period = values[1]
		self.exec_time = values[2]
		self.deadline = values[3]
		self.jobCount = 0

# # test code
# filename = 'HW1table1-1.txt'
# T = TaskSet()
# T.updateTasks(filename)

# # T.calculateHyperperiod()
# # print(T.hyperperiod)

# frames_calc = T.getFrameSizes()
# T.updateJobCount()
# print(T.tasks[38].period, T.tasks[38].jobCount)



