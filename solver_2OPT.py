from parse import read_input_file, write_output_file
import os
import random
import math
from exp_utils import get_logger
from Task import Task
import datetime
import numpy as np
import pickle
import time


# random.seed(123)
work_dir = "./logs"
now = datetime.datetime.now()
logging = get_logger(os.path.join(work_dir, now.strftime('%Y-%m-%d %H:%M:%S') + ' log.txt'))

total_benefit = 0



def solve(tasks, input_path):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    ############################################## CONFIG ##############################################    
    global opt_dict
    MAX_TIME = 1440
    opt = opt_dict.get(input_path, [None, float('-inf')])
    best_plan = opt[0]
    best_plan_benefit = opt[1]
    opt_changed = False

    ####################################################################################################
    epoch_idx = 0

    def fitness(output_tasks, tasks):
        MAX_TIME = 1440
        time_cum = 0
        benefit_cum = 0
        idx = 0
        while idx < len(tasks) and time_cum + tasks[output_tasks[idx] - 1].duration <= MAX_TIME:
            id = output_tasks[idx] - 1
            time_cum = time_cum + tasks[id].duration
            if time_cum <= tasks[id].deadline:
                benefit_cum += tasks[id].perfect_benefit
            else:
                benefit_cum += tasks[id].perfect_benefit * math.exp(-0.0170 * (time_cum - tasks[id].deadline))
            idx += 1
        return benefit_cum

    def postprocessing(output_tasks, tasks):
        idx = 0
        MAX_TIME = 1440
        time_cum = 0
        processed_output_taskId = []
        while idx < len(output_tasks) and time_cum + tasks[output_tasks[idx] - 1].duration <= MAX_TIME:
            id = output_tasks[idx] - 1
            time_cum = time_cum + tasks[id].duration
            processed_output_taskId.append(tasks[id].task_id)
            idx += 1
        return processed_output_taskId

    same = 0
    count = 0

    ############################## Initial Input ################################################
    # curr_output_tasks = [i for i in range(1, len(tasks)+1)]
    # random.shuffle(curr_output_tasks)
    tasks_greedy = sorted(tasks, key = lambda task: (round(-task.perfect_benefit / task.duration, 1), task.deadline))
    curr_output_tasks = [task.task_id for task in tasks_greedy]
    # curr_output_tasks = []
    ############################## TO CHANGE ####################################################
    start = time.time()
    early_abort_epoch = 20
    while True:
        curr_benefit = fitness(curr_output_tasks, tasks)
        exit_curr_loop = False

        i, j, k = random.sample(range(1, len(tasks)), 3)
        curr_output_tasks[i], curr_output_tasks[j], curr_output_tasks[k] = curr_output_tasks[k], curr_output_tasks[i], curr_output_tasks[j]
        
        while True:
            curr_benefit = fitness(curr_output_tasks, tasks)
            for i in range(len(tasks)):
                for j in range(i+1, len(tasks)):
                    less_raito = tasks[curr_output_tasks[j]-1].get_benefit_over_duration_ratio() < tasks[curr_output_tasks[i]-1].get_benefit_over_duration_ratio()
                    later_ddl = tasks[curr_output_tasks[j]-1].deadline > tasks[curr_output_tasks[i]-1].deadline
                    if less_raito and later_ddl:
                        continue
                    new_output_task = curr_output_tasks[:]
                    new_output_task[i], new_output_task[j] = new_output_task[j], new_output_task[i]
                    new_benefit = fitness(new_output_task, tasks)
                    if new_benefit > curr_benefit:
                        curr_output_tasks = new_output_task
                        curr_benefit = new_benefit
                        exit_curr_loop = True
                        break
                if exit_curr_loop:
                    break
            if exit_curr_loop == False:
                break
            epoch_idx += 1
            exit_curr_loop = False
        if curr_benefit > best_plan_benefit:
            best_plan_benefit = curr_benefit
            best_plan = curr_output_tasks
            same = 0
        else:
            same += 1
        if same > early_abort_epoch:
            break
        end = time.time()
        elapsed = end - start
        count = count + 1
        print(f"{count}. epoch: {epoch_idx} benefit: {curr_benefit} time: {elapsed} best: {best_plan_benefit}")
        epoch_idx = 0

    end = time.time()
    elapsed = end - start
    best_plan = postprocessing(best_plan, tasks)
    opt_dict[input_path] = (best_plan, best_plan_benefit)

    print(f"benefit: {best_plan_benefit} time: {elapsed}")

    return best_plan, best_plan_benefit
    
    


inputs_categories = ["large", "medium", "small"]

# print(os.listdir('inputs/'))

# Load optimal output
opt_dict = {}
if os.path.exists("optimum_output.pickle"):
    with open("optimum_output.pickle", "rb") as f:
        opt_dict = pickle.load(f)

task_idx = 0
for inputs_category in inputs_categories:
    for file_name in os.listdir(os.path.join('inputs/', inputs_category)):
        if file_name[0] == ".":
            continue
        input_path = 'inputs/' + inputs_category + "/" + file_name
        print(f"task {task_idx}: {input_path}")
        output_path = 'outputs/' + inputs_category + "/" + file_name[:-3] + '.out'
        tasks = read_input_file(input_path)
        output, benefit = solve(tasks, input_path)
        total_benefit = total_benefit + benefit
        
        write_output_file(output_path, output)
        task_idx += 1

# task_idx = 0
# inputs_category = "large"
# file_name = "large-1.in"
# input_path = 'inputs/' + inputs_category + "/" + file_name
# print(f"task {task_idx}: {input_path}")
# output_path = 'outputs/' + inputs_category + "/" + file_name[:-3] + '.out'
# tasks = read_input_file(input_path)
# output, benefit = solve(tasks, input_path)
# total_benefit = total_benefit + benefit

write_output_file(output_path, output)

logging(str(total_benefit))

with open('optimum_output.pickle', 'wb') as f:
    pickle.dump(opt_dict, f)

# Here's an example of how to run your solver.
# if __name__ == '__main__':
#     for input_path in os.listdir('inputs/'):
#         output_path = 'outputs/' + input_path[:-3] + '.out'
#         tasks = read_input_file(input_path)
#         output = solve(tasks)
#         write_output_file(output_path, output)
