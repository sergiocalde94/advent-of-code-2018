from collections import defaultdict
import itertools as it


def answer_function_part_one(filename: str) -> int:
    with open(filename) as frequency_changes:
        frequencies = map(lambda x: int(x[:-1]),
                          frequency_changes)
        answer_first = sum(frequencies)
    return answer_first


def answer_function_part_two(filename: str) -> int:
    def is_repeated(occurrences: defaultdict, frequency_change: int) -> bool:
        occurrences[frequency_change] += 1
        return occurrences[frequency_change] != 2

    with open(filename) as frequency_changes:
        occurrences = defaultdict(int)
        frequencies = map(lambda x: int(x[:-1]),
                          frequency_changes)
        list(it.takewhile(lambda frequency_change: is_repeated(occurrences, frequency_change),
                          it.accumulate(it.chain([0], it.cycle(frequencies)))))
        answer_second = [key for key, value in occurrences.items() if value == 2][0]
    return answer_second

if __name__ == '__main__':
    FILENAME = 'input.txt'
    answer_first = answer_function_part_one(FILENAME)
    answer_second = answer_function_part_two(FILENAME)

    print(f'First answer: {answer_first}')
    print(f'Second answer: {answer_second}')
