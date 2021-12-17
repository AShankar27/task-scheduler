import numpy as np
import matplotlib.pyplot as plt
import random
from tasks import TaskSet
from model import Q_module

filename = 'HW1table1-1.txt'
T = TaskSet()
T.updateTasks(filename)

q_model = Q_module()
q_model.updateActions(T.tasks)

q_model.train(500)
q_model.visualizeReward()

