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



2. Use Greedy to early eliminate some Tasks, then use DP in the remaining Tasks. Possible subfunction: f(time_left, task_left).


