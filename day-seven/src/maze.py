import re
import collections
import functools as ft
import itertools as it

REGEX_PARSE = r'Step (.) must be finished before step (.) can begin\.'


def parse_maze(filename: str) -> collections.defaultdict:
    steps_dict = collections.defaultdict(list)
    with open(filename) as file:
        for line in file:
            match = re.match(REGEX_PARSE, line)
            steps_dict[match[1]].append(match[2])
    return steps_dict


def get_prerequisites(
        steps_dict: collections.defaultdict) -> collections.defaultdict:
    prerequisites = collections.defaultdict(list)
    for index, next_steps in steps_dict.items():
        for step in next_steps:
            prerequisites[step].append(index)
    return prerequisites


def check_prerequisites(prerequisites: collections.defaultdict,
                        path: str,
                        step_to_be_checked: str) -> bool:
    return not set(prerequisites[step_to_be_checked]).difference(path)


def get_possible_options(steps_dict: collections.defaultdict,
                         path: str):
    return (
        sorted(
            set(steps_dict.keys())
            .union(set(ft.reduce(lambda a, b: a + b, steps_dict.values())))
            .difference(set(path))
        )
    )


def fill_path(steps_dict: collections.defaultdict,
              prerequisites: collections.defaultdict,
              path: str) -> (str, [str], bool):
    path_new = path
    path_options_sorted = get_possible_options(steps_dict, path_new)
    if not path_options_sorted:
        return path, True
    for path_option in path_options_sorted:
        if check_prerequisites(prerequisites, path, path_option):
            path_new += path_option
            break
    return path_new, False


def get_first_step(steps_dict: collections.defaultdict) -> str:
    return sorted(
        set(steps_dict.keys())
        .difference(set(ft.reduce(lambda a, b: a + b,
                                  steps_dict.values())))
    )[0]


def get_path_from_first(steps_dict: collections.defaultdict,
                        prerequisites: collections.defaultdict,
                        first_step: str) -> str:
    end = False
    path = first_step
    while not end:
        path, end = fill_path(steps_dict,
                              prerequisites,
                              path)
    return path


def get_path_multiple_workers(steps_dict: collections.defaultdict,
                              prerequisites: collections.defaultdict,
                              num_workers: int,
                              offset: int) -> int:
    workers = [dict(id=i, is_working=False, timer=0, step='')
               for i in range(num_workers)]
    path = ''
    seconds = 1
    for worker in it.cycle(workers):
        seconds += 1
        current_steps = filter(lambda p: check_prerequisites(prerequisites,
                                                             path,
                                                             p),
                               get_possible_options(steps_dict, path))
        if worker['is_working']:
            worker['timer'] -= 1
            if worker['timer'] == 0:
                path += worker['step']
                worker['is_working'] = False
        # This is not an else because when worker finish it can take other task
        if not worker['is_working']:
            try:
                current_steps_list = list(current_steps)
                current_steps_working = [worker['step'] for worker in workers]
                step = [step
                        for step in current_steps_list
                        if step not in current_steps_working][0]
                worker['is_working'] = True
                worker['step'] = step
                # ord('@') because we consider A to be 1, not 0
                worker['timer'] = ord(step) - ord('@') + offset
            except IndexError:
                # No more options available
                if all(not worker['is_working'] for worker in workers):
                    break
                else:
                    continue

    return seconds // num_workers - 1


def answer_function_part_one(filename: str) -> str:
    steps_dict = parse_maze(filename)
    first_step = get_first_step(steps_dict)
    prerequisites = get_prerequisites(steps_dict)
    return get_path_from_first(steps_dict, prerequisites, first_step)


def answer_function_part_two(filename: str, num_workers: int,
                             offset: int) -> int:
    steps_dict = parse_maze(filename)
    prerequisites = get_prerequisites(steps_dict)
    return get_path_multiple_workers(steps_dict,
                                     prerequisites,
                                     num_workers,
                                     offset)


if __name__ == '__main__':
    FILENAME = '../data/input.txt'
    answer_first = answer_function_part_one(FILENAME)
    answer_second = answer_function_part_two(FILENAME, 5, 60)

    print(f'First answer: {answer_first}')
    print(f'Second answer: {answer_second}')
