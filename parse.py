import Task

def read_input_file(path: str):
    """
    Reads an input file and returns a list of Task objects

    Args: 
    - path (str): path to the input file

    Output: 
    - list[Task]: list of Task objects 

    Sample usage:
    >>> tasks = parse.read_input_file('input.in')
    >>> print(tasks[0])
    Task 1 has deadline 2, duration 3, and max benefit 4.0
    >>> print(tasks[1])
    Task 2 has deadline 3, duration 4, and max benefit 5.0
    """
    with open(path) as input_file:

        input_lines = input_file.readlines()
        
        assert input_lines[0].split()[0].isdigit(), 'First line is not a valid number of tasks'
        num_tasks = int(input_lines[0].split()[0])
        assert num_tasks == len(input_lines) - 1, 'The number of tasks in the first line of ' \
            + 'the input file does not match the tasks defined in the rest of the input file'
        assert num_tasks <= 200,  'Too many tasks'
        
        tasks = []
        for i in range(1, num_tasks + 1):
            task_parameters = input_lines[i].split()

            assert len(task_parameters) == 4, 'The number of parameters in task {} is incorrect'.format(i)

            assert task_parameters[0].isdigit(), 'Task {} has an invalid task id {}'.format(i, task_parameters[0])
            assert int(task_parameters[0]) == i, 'Task {} has an invalid task id {}'.format(i, task_parameters[0])

            assert task_parameters[1].isdigit(), 'Task {} has an invalid deadline {}'.format(i, task_parameters[1])
            assert 0 < int(task_parameters[1]) <= 1440, 'Task {} has an invalid deadline {}'.format(i, task_parameters[1])

            assert task_parameters[2].isdigit(), 'Task {} has an invalid duration {}'.format(i, task_parameters[2])
            assert 0 < int(task_parameters[2]) <= 60, 'Task {} has an invalid duration {}'.format(i, task_parameters[2])

            try:
                float(task_parameters[3])
            except ValueError:
                assert False, 'Task {} has an invalid non-float max benefit {}'.format(i, task_parameters[3])

            decimal_checker = task_parameters[3].split('.')
            assert len(decimal_checker) == 1 or len(decimal_checker[1]) <= 3, 'Task {} has more than 3 decimal places in its max benefit {}'.format(i, task_parameters[3])
            assert 0 < float(task_parameters[3]) < 100.0, 'Task {} has an invalid max benefit {}'.format(i, task_parameters[3])

            task_id, deadline, duration, max_benefit = task_parameters
            task = Task.Task(int(task_id), int(deadline), int(duration), float(max_benefit))
            tasks.append(task)
        return tasks

def write_input_file(path: str, tasks)-> None:
    """
    Takes a path and list of Task objects and 
    generates the corresponding input file

    Note: The task objects in the tasks list must
    be in order, i.e., the task object at index i 
    must have task_id i for all i 

    Args: 
    - path (str): path to the input file
    - tasks (List[Task]): list of Task objects 

    Output:
    - None

    Sample usage:
    >>> import parse
    >>> import Task
    >>> t1 = Task.Task(1, 2, 3, 4.0)
    >>> t2 = Task.Task(2, 3, 4, 5.0)
    >>> t = [t1, t2]
    >>> parse.write_input_file('input.in', t)
    """
    num_tasks = len(tasks)

    input_lines = []
    input_lines.append(str(num_tasks) + '\n')

    for i in range(1, num_tasks + 1):

        task = tasks[i - 1]
        task_parameters = [str(task.get_task_id()), str(task.get_deadline()), str(task.get_duration()), str(task.get_max_benefit())]
        
        assert task_parameters[0].isdigit(), 'Task {} has an invalid task id {}'.format(i, task_parameters[0])
        assert int(task_parameters[0]) == i, 'Task {} has an invalid task id {}'.format(i, task_parameters[0])
        
        assert task_parameters[1].isdigit(), 'Task {} has an invalid deadline {}'.format(i, task_parameters[1])
        assert 0 < int(task_parameters[1]) <= 1440, 'Task {} has an invalid deadline {}'.format(i, task_parameters[1])
        
        assert task_parameters[2].isdigit(), 'Task {} has an invalid duration {}'.format(i, task_parameters[2])
        assert 0 < int(task_parameters[2]) <= 60, 'Task {} has an invalid duration {}'.format(i, task_parameters[2])
        
        try:
            float(task_parameters[3])
        except ValueError:
            assert False, 'Task {} has an invalid non-float max benefit {}'.format(i, task_parameters[3])

        decimal_checker = task_parameters[3].split('.')
        assert len(decimal_checker) == 1 or len(decimal_checker[1]) <= 3, 'Task {} has more than 3 decimal places in its max benefit {}'.format(i, task_parameters[3])
        assert 0 < float(task_parameters[3]) < 100.0, 'Task {} has an invalid max benefit {}'.format(i, task_parameters[3])

        input_line = '{} {} {} {}\n'.format(str(task.get_task_id()), str(task.get_deadline()), str(task.get_duration()), str(task.get_max_benefit()))
        input_lines.append(input_line)

    input_file = open(path, 'w')
    input_file.writelines(input_lines)
    input_file.close()

def read_output_file(path: str):
    """
    Reads an output file and returns a list of
    task_ids of tasks scheduled in order

    Note: This function simply checks that each
    line of your output has a single task_id < 200
    and that no task_id has been repeated

    Args: 
    - path (str): path to the input file

    Output:
    - List[int]: list of task_ids

    Sample usage:
    >>> task_ids_scheduled = parse.read_output_file('output.out')
    >>> task_ids_scheduled
    [1, 2]
    """
    task_ids = set()
    task_ids_scheduled = []

    with open(path) as input_file:

        input_lines = input_file.readlines()

        num_tasks = len(input_lines)
        assert num_tasks <= 200, 'Too many tasks scheduled. ' \
            + 'Make sure you are not repeating any tasks.'
        
        for i in range(num_tasks):

            assert len(input_lines[i].split()) == 1, 'Invalid number of items on line {}'.format(i + 1)

            task_id = input_lines[i].split()[0]
            assert task_id.isdigit(), 'Invalid task_id {}'.format(task_id)
            assert 1 <= int(task_id) <= 200, 'Invalid task_id {}'.format(task_id)
            assert task_id not in task_ids, 'task_id {} appears more than once'.format(task_id)

            task_id = int(task_id)
            task_ids.add(task_id)
            task_ids_scheduled.append(task_id)
    
    return task_ids_scheduled
    
def write_output_file(path: str, task_ids):
    """
    Takes a path and list of task_ids and 
    generates the corresponding output file

    Args: 
    - path (str): path to the input file
    - tasks (List[int]): list of task_ids
    
    Output:
    - None

    Sample usage:
    >>> task_ids = [1, 2]
    >>> parse.write_output_file('output.out', task_ids)
    """
    assert len(task_ids) <= 200, 'Too many tasks scheduled. ' \
            + 'Make sure you are not repeating any tasks.'

    output_lines = []

    for task_id in task_ids:

        assert type(task_id) == int, 'task_id {} is invalid'.format(task_id)
        assert 1 <= task_id <= 200, 'task_id {} is invalid'.format(task_id)

        output_lines.append("{}\n".format(str(task_id)))

    output_file = open(path, 'w')
    output_file.writelines(output_lines)
    output_file.close()