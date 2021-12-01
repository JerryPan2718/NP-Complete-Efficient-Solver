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
    ############################################## CONFIG ##############################################    
    global opt_dict
    MAX_TIME = 1440
    n_round = 1
    opt = opt_dict.get(input_path, [None, float('-inf')])
    best_plan = opt[0]
    best_plan_benfit = opt[1]
    opt_changed = False

    ####################################################################################################
    def calculate_probabilty_distribution_linear(discounted_profit_tasks):
        discounted_profit_tasks_sum = sum(discounted_profit_tasks)
        discounted_profit_proportion_tasks = [task_profit / discounted_profit_tasks_sum for task_profit in discounted_profit_tasks]
        return discounted_profit_proportion_tasks

    def calculate_probabilty_distribution_softmax(discounted_profit_tasks):
        discounted_profit_proportion_tasks = np.exp(np.array(discounted_profit_tasks)) / np.sum(np.exp(np.array(discounted_profit_tasks)))
        return discounted_profit_proportion_tasks

    def calculate_probabilty_distribution_random(discounted_profit_tasks):
        n = len(discounted_profit_tasks)
        return [1/n for _ in range(n)]

    def calculate_probabilty_distribution_linear_activation(discounted_profit_tasks):
        discounted_profit_tasks_mean = np.mean(discounted_profit_tasks)
        discounted_profit_proportion_tasks = []
        for task_profit in discounted_profit_tasks:
            if task_profit >= discounted_profit_tasks_mean:
                discounted_profit_proportion_tasks.append(task_profit)
            else:
                discounted_profit_proportion_tasks.append(0)
        
        # discounted_profit_proportion_tasks = np.array(discounted_profit_proportion_tasks) / np.sum(np.array(discounted_profit_proportion_tasks))
        discounted_profit_tasks_sum = sum(discounted_profit_tasks)
        if discounted_profit_tasks_sum != 0:
            discounted_profit_proportion_tasks = [task_profit / discounted_profit_tasks_sum for task_profit in discounted_profit_tasks]
        else:
            discounted_profit_proportion_tasks = [1/len(discounted_profit_tasks) for _ in range(len(discounted_profit_tasks))]
            # print(sum(discounted_profit_proportion_tasks))
        return discounted_profit_proportion_tasks

    def calculate_probabilty_distribution_softmax_activation(discounted_profit_tasks):
        discounted_profit_tasks_mean = np.mean(discounted_profit_tasks)
        discounted_profit_proportion_tasks = []
        for task_profit in discounted_profit_tasks:
            if task_profit >= discounted_profit_tasks_mean:
                discounted_profit_proportion_tasks.append(task_profit)
            else:
                discounted_profit_proportion_tasks.append(0)
        
        # discounted_profit_proportion_tasks = np.array(discounted_profit_proportion_tasks) / np.sum(np.array(discounted_profit_proportion_tasks))
        discounted_profit_tasks_sum = sum(discounted_profit_tasks)
        if discounted_profit_tasks_sum != 0:
            discounted_profit_proportion_tasks = [task_profit / discounted_profit_tasks_sum for task_profit in discounted_profit_tasks]
        else:
            discounted_profit_proportion_tasks = [1/len(discounted_profit_tasks) for _ in range(len(discounted_profit_tasks))]

        discounted_profit_proportion_tasks = np.array(discounted_profit_proportion_tasks) / np.sum(np.array(discounted_profit_proportion_tasks))
        # print(sum(discounted_profit_proportion_tasks))
        return discounted_profit_proportion_tasks
    ####################################################################################################
    for _ in range(n_round):
        output_tasks = []
        remaining_tasks = tasks[:]
        idx = 0
        time_cum = 0
        benefit_cum = 0
        while remaining_tasks and time_cum <= MAX_TIME:
            discounted_profit_tasks = []
            remaining_tasks = [task for task in remaining_tasks if task.duration + time_cum <= MAX_TIME]
            if not remaining_tasks:
                break
            for i in range(len(remaining_tasks)):
                remaining_task = remaining_tasks[i]
                if time_cum <= remaining_task.deadline:
                    benefit = remaining_task.perfect_benefit
                else:
                    benefit = remaining_task.perfect_benefit * math.exp(-0.0170 * (time_cum - remaining_task.deadline))
                discounted_profit_tasks.append(benefit)
            
            tasks_probability_distribution = calculate_probabilty_distribution_linear_activation(discounted_profit_tasks)
            max_discounted_profit_task = np.random.choice(remaining_tasks, p=tasks_probability_distribution)

            output_tasks.append(max_discounted_profit_task.task_id)
            time_cum += max_discounted_profit_task.duration

            if time_cum <= max_discounted_profit_task.deadline:
                benefit = max_discounted_profit_task.perfect_benefit
            else:
                benefit = max_discounted_profit_task.perfect_benefit * math.exp(-0.0170 * (time_cum - max_discounted_profit_task.deadline))
            benefit_cum += benefit

            remaining_tasks.remove(max_discounted_profit_task)
    if benefit_cum > best_plan_benfit:
        opt_changed = True
        best_plan_benfit = benefit_cum
        best_plan = output_tasks
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

# for inputs_category in inputs_categories:
#     for file_name in os.listdir(os.path.join('inputs/', inputs_category)):
#         if file_name[0] == ".":
#             continue
#         input_path = 'inputs/' + inputs_category + "/" + file_name
#         # print(input_path)
#         output_path = 'outputs/' + inputs_category + "/" + file_name[:-3] + '.out'
#         tasks = read_input_file(input_path)
#         output, benefit = solve(tasks, input_path)
#         total_benefit = total_benefit + benefit
#         # print(output_path)
#         write_output_file(output_path, output)


input_path = 'inputs/' + "small" + "/" + "small-1.in"
# print(input_path)
output_path = 'outputs/' + "small" + "/" + "small-1.out"
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
