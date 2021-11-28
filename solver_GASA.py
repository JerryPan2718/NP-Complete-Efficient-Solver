from parse import read_input_file, write_output_file
import os
import random
import math
from exp_utils import get_logger
import datetime

random.seed(123)
work_dir = "./logs"
now = datetime.datetime.now()
logging = get_logger(os.path.join(work_dir, now.strftime('%Y-%m-%d %H:%M:%S') + ' log.txt'))

total_fitness = 0

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    ############################################## CONFIG ##############################################
    
    
    ####################################################################################################


    output_tasks = []
    remaining_tasks = tasks[:]
    idx = 0
    time_cum = 0
    benefit_cum = 0
    MAX_TIME = 1440
    while remaining_tasks and time_cum <= MAX_TIME:
        discounted_profit_tasks = []
        remaining_tasks = [task for task in remaining_tasks if task.duration + time_cum <= MAX_TIME]
        for i in range(len(remaining_tasks)):
            remaining_task = remaining_tasks[i]
            if time_cum <= remaining_task.deadline:
                benefit = remaining_task.perfect_benefit
            else:
                benefit = remaining_task.perfect_benefit * math.exp(-0.0170 * (time_cum - remaining_task.deadline))
            discounted_profit_tasks.append(benefit)
        
        max_discounted_profit = max(discounted_profit_tasks)
        max_discounted_profit_taskId = discounted_profit_tasks.index(max_discounted_profit)
        max_discounted_profit_task = remaining_tasks[max_discounted_profit_taskId]


        output_tasks.append(max_discounted_profit_task.task_id)
        time_cum += max_discounted_profit_task.duration
        benefit_cum += max_discounted_profit

        remaining_tasks.remove(max_discounted_profit_task)
    return output_tasks


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
        output, single_fitness = solve(tasks)
        print(output_path)
        write_output_file(output_path, output)
        total_fitness = total_fitness + single_fitness

logging(str(total_fitness))

# Here's an example of how to run your solver.
# if __name__ == '__main__':
#     for input_path in os.listdir('inputs/'):
#         output_path = 'outputs/' + input_path[:-3] + '.out'
#         tasks = read_input_file(input_path)
#         output = solve(tasks)
#         write_output_file(output_path, output)
