import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from parse import read_input_file, write_output_file
import random
import math
from exp_utils import get_logger
import datetime
import numpy as np
import pickle


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
    epoch_idx = 0

    ####################################################################################################
    

    def fitness(output_tasks, tasks):
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
        total_time = sum([tasks[taskId-1].duration for taskId in processed_output_taskId])
        return processed_output_taskId

    curr_output_tasks = [i for i in range(1, len(tasks)+1)]
    curr_benefit = fitness(curr_output_tasks, tasks)
    exit_curr_loop = False
    while True:
        curr_benefit = fitness(curr_output_tasks, tasks)
        for i in range(len(tasks)):
            for j in range(i+5, len(tasks)):
                for k in range(j+5, len(tasks)):
                    new_output_tasks1 = curr_output_tasks[:]
                    new_output_tasks2 = curr_output_tasks[:]
                    new_output_tasks3 = curr_output_tasks[:]
                    new_output_tasks4 = curr_output_tasks[:]
                    new_output_tasks5 = curr_output_tasks[:]

                    new_output_tasks1[i], new_output_tasks1[j], new_output_tasks1[k] = new_output_tasks1[j], new_output_tasks1[i], new_output_tasks1[k]
                    new_output_tasks2[i], new_output_tasks2[j], new_output_tasks2[k] = new_output_tasks2[k], new_output_tasks2[j], new_output_tasks2[i]
                    new_output_tasks3[i], new_output_tasks3[j], new_output_tasks3[k] = new_output_tasks3[i], new_output_tasks3[k], new_output_tasks3[j]
                    new_output_tasks4[i], new_output_tasks4[j], new_output_tasks4[k] = new_output_tasks4[j], new_output_tasks4[k], new_output_tasks4[i]
                    new_output_tasks5[i], new_output_tasks5[j], new_output_tasks5[k] = new_output_tasks5[k], new_output_tasks5[i], new_output_tasks5[j]


                    new_benefit1 = fitness(new_output_tasks1, tasks)
                    new_benefit2 = fitness(new_output_tasks2, tasks)
                    new_benefit3 = fitness(new_output_tasks3, tasks)
                    new_benefit4 = fitness(new_output_tasks4, tasks)
                    new_benefit5 = fitness(new_output_tasks5, tasks)

                    new_benefits = [new_benefit1, new_benefit2, new_benefit3, new_benefit4, new_benefit5]
                    new_output_tasks = [new_output_tasks1, new_output_tasks2, new_output_tasks3, new_output_tasks4, new_output_tasks5]

                    for i in range(len(new_benefits)):
                        new_benefit = new_benefits[i]
                        new_output_task = new_output_tasks[i]
                        if new_benefit > curr_benefit:
                            curr_output_tasks = new_output_task[:]
                            curr_benefit = new_benefit
                            exit_curr_loop = True
                            break
                if exit_curr_loop:
                    break
            if exit_curr_loop:
                break
        if exit_curr_loop == False:
            break
        epoch_idx += 1
        exit_curr_loop = False
        # print(f"epoch {epoch_idx}: benefit {curr_benefit}")
    if curr_benefit > best_plan_benefit:
        opt_changed = True
        best_plan_benefit = curr_benefit
        best_plan = postprocessing(curr_output_tasks, tasks)
    if opt_changed:
        opt_dict[input_path] = (best_plan, best_plan_benefit)
    print(f"epoch {epoch_idx}: benefit {best_plan_benefit}")
    return best_plan, best_plan_benefit
    

inputs_categories = ["large", "medium", "small"]

print(os.listdir('inputs/'))

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
        print(output_path)
        write_output_file(output_path, output)
        task_idx += 1

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
