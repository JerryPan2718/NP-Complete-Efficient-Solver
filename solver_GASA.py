from parse import read_input_file, write_output_file
import os
import random
import math
from exp_utils import get_logger
import datetime
import numpy as np

random.seed(123)
work_dir = "./logs"
now = datetime.datetime.now()
logging = get_logger(os.path.join(work_dir, now.strftime('%Y-%m-%d %H:%M:%S') + ' log.txt'))

total_benefit = 0

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    ############################################## CONFIG ##############################################
    
    
    ####################################################################################################


    MAX_TIME = 1440
    n_round = 100
    best_plan = None
    best_plan_benfit = float("-inf")

    ####################################################################################################
    def calculate_probabilty_distribution(discounted_profit_tasks):
        discounted_profit_tasks_sum = sum(discounted_profit_tasks)
        discounted_profit_proportion_tasks = [task_profit / discounted_profit_tasks_sum for task_profit in discounted_profit_tasks]
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
            
            tasks_probability_distribution = calculate_probabilty_distribution(discounted_profit_tasks)
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
        best_plan_benfit = benefit_cum
        best_plan = output_tasks
    return best_plan, best_plan_benfit


inputs_categories = ["large", "medium", "small"]

print(os.listdir('inputs/'))
for inputs_category in inputs_categories:
    for file_name in os.listdir(os.path.join('inputs/', inputs_category)):
        if file_name[0] == ".":
            continue
        input_path = 'inputs/' + inputs_category + "/" + file_name
        print(input_path)
        output_path = 'outputs/' + inputs_category + "/" + file_name[:-3] + '.out'
        tasks = read_input_file(input_path)
        output, benefit = solve(tasks)
        total_benefit = total_benefit + benefit
        print(output_path)
        write_output_file(output_path, output)

logging(str(total_benefit))

# Here's an example of how to run your solver.
# if __name__ == '__main__':
#     for input_path in os.listdir('inputs/'):
#         output_path = 'outputs/' + input_path[:-3] + '.out'
#         tasks = read_input_file(input_path)
#         output = solve(tasks)
#         write_output_file(output_path, output)
