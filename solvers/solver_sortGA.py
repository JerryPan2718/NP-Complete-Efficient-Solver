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
    num_generations = 0 # Doesn't matter
    mutation_rate = 100 # Initially big then small
    offspring_size = 100 # Big
    keep_top_k = 100 # Big
    
    ####################################################################################################

    # print(tasks)
    # Greedy Algorithm as the initial genome for Genetic Algorithm
    # 4 Attributes of Task:         
    # task_id, deadline, duration, perfect_benefit

    # print(tasks[0])
    # print([task.task_id for task in tasks]) 
    # print(len(tasks))


    tasks_greedy = sorted(tasks, key = lambda task: (round(-task.perfect_benefit / task.duration, 1), task.deadline))
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
        while idx < len(tasks) and time_cum + tasks[output_tasks[idx] - 1].duration <= MAX_TIME:
            id = output_tasks[idx] - 1
            time_cum = time_cum + tasks[id].duration
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
        total_time = sum([tasks[taskId-1].duration for taskId in processed_output_taskId])
        time_exceeded = total_time > 1440
        # print(time_cum, total_time, time_exceeded)
        # print(processed_output_taskId)
        return processed_output_taskId

    # Main
    rankedSolutions = [(initial_output_tasks, fitness(initial_output_tasks, tasks))]
    new_generation = []
    for i in range(num_generations):
        for batch in range(offspring_size):
            for idx, s in enumerate(rankedSolutions):
                mutated_output_tasks = mutate(s[0])
                new_generation.append((mutated_output_tasks, fitness(mutated_output_tasks, tasks)))
        new_generation = new_generation + rankedSolutions
        new_generation.sort(key=lambda solution: -solution[1]) # Sort by the decreasing order of fitness

        rankedSolutions = new_generation[:keep_top_k]
        new_generation = []
        rankedSolutions_fitness = sum([solutions[1] for solutions in rankedSolutions])
        logging(f"=== Gen {i} best solutions with fitness {rankedSolutions[0][1]} and overall fitness {rankedSolutions_fitness} ===")
    
    # total_fitness = total_fitness + rankedSolutions[0][1]
    task_order_for_output = postprocessing(rankedSolutions[0][0], tasks)
    return task_order_for_output, rankedSolutions[0][1]

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
