from parse import read_input_file, write_output_file
import os
import random
import math
from exp_utils import get_logger
import datetime
import numpy as np
import pickle
import cvxpy as cp


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

    # variables: length n array of starting time
    # objective: max of sum of compute_benefit() called on all tasks
    # constraint: 
    #   j.order[i] + i.order[j] == 1 for all i, j where i != j
    #   j.order[i] * (t_i.task_start_time - t_j.task_start_time - t_j.duration) + i.order[j] * (t_j.task_start_time - t_i.task_start_time - t_i.duration > 0) >= 0
    # Note: j.order[i] = 1 if j < i, j.order[i] = 0 if j > i
    
    def compute_benefit(task, task_start_time):
        # if task_start_time + task.duration <= task.deadline:
        #     return task.perfect_benefit
        # else:
        # return task.perfect_benefit * math.exp(-0.0170 * (task_start_time + task.duration - task.deadline))
        return 1

    # variables
    # variable_list: [t1.start_time, t2.start_time,..., tn.start_time, t1.order(t1), t1.order(t2), ..., tn.order(tn)]
    variable_list = []
    for _ in range(len(tasks) + len(tasks) * len(tasks)):
        variable_list.append(cp.Variable())

    # function
    def objective_function(variable_list):
        return sum([compute_benefit(tasks[i], variable_list[i]) for i in range(len(tasks))])

    obj = cp.Maximize(objective_function(variable_list))

    # constraints
    constraints = []
    
    order_lists = np.reshape(variable_list[len(tasks):], (len(tasks), len(tasks)))
    for i in range(len(tasks)):
        constraints.append(variable_list[i] >= 0)
        for j in range(len(tasks)):
            if i != j:
                # order constraints
                constraints.append(order_lists[j][i] >= 0)
                # constraints.append(order_lists[j][i] <= 1)
                constraints.append(order_lists[i][j] + order_lists[j][i] == 1)
                # start time and duration constraints
                constraints.append(order_lists[j][i] * (variable_list[i] - variable_list[j] - tasks[j].duration) + \
                                    order_lists[i][j] * (variable_list[j] - variable_list[i] - tasks[i].duration) >= 0 )

    prob = cp.Problem(obj, constraints)
    prob.solve()  # Returns the optimal value.
    print("status:", prob.status)
    print("optimal value", prob.value)
    # print("optimal var", x.value, y.value)
    
    


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
