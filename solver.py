from parse import read_input_file, write_output_file
import os

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    ############################################## CONFIG ##############################################
    num_generations = 10000
    mutation_rate = 2
    batch_size = 100
    keep_top_k = 100
    
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
    # print([task.task_id for task in tasks_greedy]) 

    ## Genetic Algorithm
    def fitness(output_tasks, tasks):
        return sum([tasks[task-1].perfect_benefit for task in output_tasks[50:]]) # Dummy function
        pass

    def mutate(output_tasks):
        length_output_tasks = len(output_tasks)
        return output_tasks

    print(tasks)
    print(fitness(initial_output_tasks, tasks))
    rankedSolutions = [(initial_output_tasks, fitness(initial_output_tasks, tasks))]
    new_generation = []
    for i in range(num_generations):
        for batch in range(batch_size):
            for s in rankedSolutions:
                mutated_output_tasks = mutate(s[0])
                new_generation.append((mutated_output_tasks, fitness(mutated_output_tasks, tasks)))
        new_generation.sort(key=lambda solution: -solution[1]) # Sort by the decreasing order of fitness

        rankedSolutions = new_generation[:keep_top_k]
        new_generation = []

        print(f"=== Gen {i} best solutions with fitness {rankedSolutions[0]} ===") 

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