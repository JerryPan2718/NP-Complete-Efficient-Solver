from parse import read_input_file, read_output_file, write_output_file
import os
import random
import math
from exp_utils import get_logger
from Task import Task
import datetime
import pickle
import time

def fitness(output_tasks, tasks):
        assert len(output_tasks) == len(set(output_tasks)), "output_tasks contain duplicates!"
        MAX_TIME = 1440
        time_cum = 0
        benefit_cum = 0
        idx = 0
        while idx < len(output_tasks) and time_cum + tasks[output_tasks[idx] - 1].duration <= MAX_TIME:
            id = output_tasks[idx] - 1
            time_cum = time_cum + tasks[id].duration
            if time_cum <= tasks[id].deadline:
                benefit_cum += tasks[id].perfect_benefit
            else:
                benefit_cum += tasks[id].perfect_benefit * math.exp(-0.0170 * (time_cum - tasks[id].deadline))
            idx += 1
        if idx != len(output_tasks):
            print("time limit exceeded")
        return benefit_cum

def log_benefit(size, num):
    tasks = read_input_file("inputs/{0}/{0}-{1}.in".format(size, num))
    output = read_output_file("outputs/{0}/{0}-{1}.out".format(size, num))
    # output = "84\n128\n141\n44\n119\n107\n19\n76\n82\n36\n4\n34\n7\n24\n145\n95\n133\n132\n112\n159\n120\n113\n53\n33\n46\n8\n6\n68\n117\n131\n38\n130\n127\n116\n10\n62\n90\n86\n178\n106\n60\n122\n93\n57\n61\n52\n96\n138\n114\n64\n161\n74\n65\n83\n2\n118\n25\n121\n147\n54\n50\n165\n143\n37\n149\n173\n155\n12\n"
    print("{0}-{1}:".format(size, num), fitness(output, tasks))

log_benefit("large", 160)
log_benefit("large", 131)
log_benefit("small", 217)