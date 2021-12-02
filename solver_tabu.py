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
    global full_opt_dict
    MAX_TIME = 1440
    opt = opt_dict.get(input_path, [None, float('-inf')])
    best_plan = opt[0]
    best_plan_benefit = opt[1]
    opt_changed = False
    max_tabu_length = 30

    ####################################################################################################

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

    def neighbors(output_tasks):
        neighbors = []
        for i in range(len(output_tasks)):
            for j in range(i + 1, len(output_tasks)):
                temp = output_tasks[:]
                temp[i], temp[j] = temp[j], temp[i]
                neighbors.append(temp)
        return neighbors

    ############################## Initial Input ################################################
    curr_output_tasks = best_plan
    to_append_for_curr_output_tasks = []
    for task in tasks:
        if task.task_id not in best_plan:
            to_append_for_curr_output_tasks.append(task.task_id)
    random.shuffle(to_append_for_curr_output_tasks)
    curr_output_tasks = curr_output_tasks + to_append_for_curr_output_tasks
    best_plan = best_plan_candidate = curr_output_tasks
    tabu_list = [curr_output_tasks]
    ############################## TO CHANGE ####################################################

    early_abort_epoch = 20
    unchanged_iteration = 0
    iteration_num = 0

    while True:
        curr_output_neighbors = neighbors(curr_output_tasks)
        best_plan_candidate = curr_output_neighbors[0]
        for candidate_output in curr_output_neighbors:
            if (not candidate_output in tabu_list) and fitness(candidate_output, tasks) > fitness(best_plan_candidate, tasks):
                best_plan_candidate = candidate_output[:]
        print("best_plan_candidate_fitness:", fitness(best_plan_candidate, tasks))
        if fitness(best_plan_candidate, tasks) > fitness(best_plan, tasks):
            best_plan = best_plan_candidate[:]
            unchanged_iteration = 0
        else:
            unchanged_iteration += 1
        tabu_list.append(best_plan_candidate)
        if len(tabu_list) > max_tabu_length:
            tabu_list.pop(0)
        if unchanged_iteration > early_abort_epoch:
            break
        iteration_num += 1
        print(f"{iteration_num}. benefit: {fitness(best_plan, tasks)}")

    full_opt_dict[input_path] = (best_plan[:], best_plan_benefit)
    best_plan = postprocessing(best_plan, tasks)
    best_plan_benefit = fitness(best_plan, tasks)
    if best_plan_benefit > opt_dict[input_path][1]:
        opt_dict[input_path] = [best_plan, best_plan_benefit]

    return postprocessing(best_plan, tasks), fitness(best_plan, tasks)

inputs_categories = ["large", "medium", "small"]

# print(os.listdir('inputs/'))

# Load optimal output
opt_dict = {}
if os.path.exists("optimum_output.pickle"):
    with open("optimum_output.pickle", "rb") as f:
        opt_dict = pickle.load(f)

full_opt_dict = {}
if os.path.exists("full_optimum_output.pickle"):
    with open("full_optimum_output.pickle") as f:
        full_opt_dict = pickle.load(f)

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

with open('full_optimum_output.pickle', 'wb') as f:
    pickle.dump(full_opt_dict, f)

# Here's an example of how to run your solver.
# if __name__ == '__main__':
#     for input_path in os.listdir('inputs/'):
#         output_path = 'outputs/' + input_path[:-3] + '.out'
#         tasks = read_input_file(input_path)
#         output = solve(tasks)
#         write_output_file(output_path, output)
