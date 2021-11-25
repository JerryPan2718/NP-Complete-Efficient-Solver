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

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    ############################################## CONFIG ##############################################
    num_generations = 10000 # Doesn't matter
    mutation_rate = 10 # Initially big then small
    offspring_size = 1000 # Big
    keep_top_k = 1000 # Big
    
    ####################################################################################################

    # print(tasks)
    # Greedy Algorithm as the initial genome for Genetic Algorithm
    # 4 Attributes of Task:         
    # task_id, deadline, duration, perfect_benefit

    # print(tasks[0])
    # print([task.task_id for task in tasks]) 
    # print(len(tasks))


    tasks_greedy = sorted(tasks, key = lambda task: (-task.perfect_benefit / task.duration, task.deadline))
    initial_output_tasks = [task.task_id for task in tasks_greedy]
    # initial_output_tasks = [i for i in range(100)]


    # print([task.task_id for task in tasks_greedy]) 

    ## Genetic Algorithm
    def fitness(output_tasks, tasks):
        # print(1)
        MAX_TIME = 1440
        time_cum = 0
        benefit_cum = 0
        idx = 0
        while time_cum + tasks[idx].duration <= MAX_TIME and idx < len(tasks):
            id = output_tasks[idx] - 1
            time_cum += tasks[id].duration
            if time_cum <= tasks[id].deadline:
                benefit_cum += tasks[id].perfect_benefit
            else:
                benefit_cum += tasks[id].perfect_benefit * math.exp(-0.0170 * (time_cum - tasks[id].deadline))
            idx += 1
            # print(benefit_cum)
        # print(benefit_cum)
        return benefit_cum

    def mutate(output_tasks):
        n = len(output_tasks)
        mutation_num = random.randint(0, mutation_rate - 1)
        for mutation in range(mutation_num):
            i, j = random.randint(0, n - 1), random.randint(0, n - 1)
            output_tasks[i], output_tasks[j] = output_tasks[j], output_tasks[i]
        return output_tasks

    # print(tasks)
    # print(fitness(initial_output_tasks, tasks))
    rankedSolutions = [(initial_output_tasks, fitness(initial_output_tasks, tasks))]
    new_generation = []
    for i in range(num_generations):
        for batch in range(offspring_size):
            for idx, s in enumerate(rankedSolutions):
                mutated_output_tasks = mutate(s[0])
                new_generation.append((mutated_output_tasks, fitness(mutated_output_tasks, tasks)))
        new_generation = new_generation + rankedSolutions
        # print(new_generation[0])
        new_generation.sort(key=lambda solution: -solution[1]) # Sort by the decreasing order of fitness
        # print(new_generation[0])

        rankedSolutions = new_generation[:keep_top_k]
        # print(rankedSolutions)
        new_generation = []

        logging(f"=== Gen {i} best solutions with fitness {rankedSolutions[0][1]} ===")

    return rankedSolutions[0]


print(os.listdir('inputs/'))
for file_name in os.listdir('inputs/'):
    input_path = 'inputs/' + file_name
    print(input_path)
    output_path = 'outputs/' + input_path[:-3] + '.out'
    tasks = read_input_file(input_path)
    output = solve(tasks)
    



# Here's an example of how to run your solver.
# if __name__ == '__main__':
#     for input_path in os.listdir('inputs/'):
#         output_path = 'outputs/' + input_path[:-3] + '.out'
#         tasks = read_input_file(input_path)
#         output = solve(tasks)
#         write_output_file(output_path, output)