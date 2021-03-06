# CS 170 Project Fall 2021

Take a look at the project spec before you get started!

Requirements:

Python 3.6+

Files:
- `parse.py`: functions to read/write inputs and outputs
- `solver.py`: where you should be writing your code to solve inputs
- `Task.py`: contains a class that is useful for processing inputs

When writing inputs/outputs:
- Make sure you use the functions `write_input_file` and `write_output_file` provided
- Run the functions `read_input_file` and `read_output_file` to validate your files before submitting!
- These are the functions run by the autograder to validate submissions


Algorithm Brainstorms:
1. Initialize a reasonably good output using Greedy Algorithm, and then use Genetic Algorithm to optimize based on our reasonably good output. (Jerry)
- loss_funtion(input_tasks, output_tasks) where "input_tasks" is an array of n tasks with all specified attributes and "output_tasks" is the order of tasks we return by the algorithm as an array of n numbers.



2. Use Greedy to early eliminate some Tasks, then use DP in the remaining Tasks. 
- subfunction: f(time_left, task_left).
- relation: f(time_left, task_left) = f(time_left - task_i.duration, task_left - task_i) + task_i.discountedProfit 
    - i based on the ranking of sorted (profit/duration)
- 1440 * (2 ** n)
- 1440 * (2 ** n / k)
- 1440 * n (submodular -> all tasks before deadlines -> n number machine scheduling problems)

3. Local swap (Edward)
- 2/3 OP
- 3 OP is really good for TSP
- while True:
    - for set_i in set_3:
        - for comb_i in all_combs (==6):
            - if new_score > curr_score:
                - curr_score = new_score
4. GRASP
5. Submodularity

Experiments:
1. Genetic Algorithm (solver_Genetic.py)
- Initialize a reasonably good output using Greedy Algorithm, and then use Genetic Algorithm to optimize based on our reasonably good output
- Takes almost infinite to run
- total_benefit = NA

2. Greedy on Sorted Rank of (profit/duration) (solver_sortGA.py)
- solver_Genetic.py with num_generation = 0
- Greedy sort by (profit/duration)
- total_benefit = 2720696.426620777

3. Greedy Discounted Profit (solver_localGA.py)
- Greedy sort by profit and take until no more valid
- total_benfit = 2719729.2186064925

4. Greedy Discounted Profit with Probability Distribution (solver_GAPD.py)
- Greedy sort by profit with probability distribution and take until no more valid
- (1) Linear (n_round=100)
- total_benfit = 2166796.452501703
- (2) Softmax (n_round=100)
- total_benfit = 2660092.022518058

5. Reduce to ILP (solver_ILP.py)

6. 2/3 OPT naive (20211129)
- total_benfit = 3504796.155992973


2/3 OPT Approach:
- Done:
    1. Naive implementation of 2/3 OPT with 1 to n unchanged initial output
    2. random.shuffle() initial output with n initializations
        - This multiple initialization could potentially turn the local maximum of 2/3 OPT into global maximum
    3. Early abort based on change of fitness() reduces runtime
    4. Initial tasks from sort greedy and local greedy + shuffle
    5. Initial tasks from pickle dictionary + shuffle
    6.  Only calculate the fitness of swapped tasks (low priority)


Replicate our algorithm for submission
```
python3 solver.py
python3 prepare_submission.py outputs/ submission.json
```
Submit the submission.json and team.txt to Gradescope
