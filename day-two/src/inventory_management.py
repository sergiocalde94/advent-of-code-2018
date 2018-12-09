import itertools as it
import collections


def parse_ids(filename: str) -> [int]:
    with open(filename) as ids:
        box_ids = map(lambda x: x[:-1], ids)
        box_ids_list = list(box_ids)
    return box_ids_list


def contains_n_times(counter: collections.Counter, n: int):
    return {value
            for value in counter
            if counter[value] == n}


def is_only_one_letter_different(id_left: str, id_right: str) -> bool:
    n = 0
    for x, y in zip(id_left, id_right):
        n += 1 if x != y else 0
        if n == 2:
            return False
    else:
        return False if n == 0 else True


def remove_different_character(str_left: str, str_right: str) -> str:
    return ''.join(char_left
                   for char_left, char_right in zip(str_left, str_right)
                   if char_left == char_right)


def answer_function_part_one(filename: str) -> int:
    box_ids = parse_ids(filename)
    number_two, number_three = 0, 0
    for box_id in box_ids:
        counter = collections.Counter(box_id)
        number_two += 1 if contains_n_times(counter, 2) else 0
        number_three += 1 if contains_n_times(counter, 3) else 0
    return number_two * number_three


def answer_function_part_two(filename: str) -> str:
    box_ids = parse_ids(filename)
    for index, box_id in enumerate(box_ids):
        for box_id_possibility in it.islice(box_ids, index, None):
            if is_only_one_letter_different(box_id, box_id_possibility):
                return remove_different_character(box_id, box_id_possibility)


if __name__ == '__main__':
    FILENAME = '../data/input.txt'
    answer_first = answer_function_part_one(FILENAME)
    answer_second = answer_function_part_two(FILENAME)

    print(f'First answer: {answer_first}')
    print(f'Second answer: {answer_second}')

