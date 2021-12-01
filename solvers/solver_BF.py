from parse import read_input_file, write_output_file
import os
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
    global opt_dict
    MAX_TIME = 1440
    n_round = 100
    n_tasks = len(tasks)
    opt = opt_dict.get(input_path, [None, float('-inf')])
    best_plan = opt[0]
    best_plan_benfit = opt[1]
    opt_changed = False

    def postprocessing(output_tasks, tasks):
        idx = 0
        MAX_TIME = 1440
        time_cum = 0
        processed_output_taskId = []
        while idx < len(tasks) and time_cum + tasks[output_tasks[idx] - 1].duration <= MAX_TIME:
            id = output_tasks[idx] - 1
            time_cum = time_cum + tasks[id].duration
            processed_output_taskId.append(tasks[id].task_id)
            idx += 1
        # total_time = sum([tasks[taskId-1].duration for taskId in processed_output_taskId])
        return processed_output_taskId

    for _ in range(n_round):
        idx = 0
        time_cum = 0
        random_output_tasks = random.sample([i for i in range(1, n_tasks+1)], n_tasks)
        processed_output_taskId = postprocessing(random_output_tasks, tasks)
        # print(1)
        time_cum = 0
        benefit_cum = 0
        idx = 0
        while idx < len(processed_output_taskId) and time_cum + tasks[processed_output_taskId[idx] - 1].duration <= MAX_TIME:
            id = processed_output_taskId[idx] - 1
            time_cum = time_cum + tasks[id].duration
            if time_cum <= tasks[id].deadline:
                benefit_cum += tasks[id].perfect_benefit
            else:
                benefit_cum += tasks[id].perfect_benefit * math.exp(-0.0170 * (time_cum - tasks[id].deadline))
            idx += 1

        if benefit_cum > best_plan_benfit:
            opt_changed = True
            best_plan_benfit = benefit_cum
            best_plan = processed_output_taskId
        if opt_changed:
            opt_dict[input_path] = (best_plan, best_plan_benfit)
    return best_plan, best_plan_benfit


inputs_categories = ["large", "medium", "small"]

print(os.listdir('inputs/'))

# Load optimal output
opt_dict = {}
if os.path.exists("optimum_output.pickle"):
    with open("optimum_output.pickle", "rb") as f:
        opt_dict = pickle.load(f)

for inputs_category in inputs_categories:
    for file_name in os.listdir(os.path.join('inputs/', inputs_category)):
        if file_name[0] == ".":
            continue
        input_path = 'inputs/' + inputs_category + "/" + file_name
        # print(input_path)
        output_path = 'outputs/' + inputs_category + "/" + file_name[:-3] + '.out'
        tasks = read_input_file(input_path)
        output, benefit = solve(tasks, input_path)
        total_benefit = total_benefit + benefit
        # print(output_path)
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
