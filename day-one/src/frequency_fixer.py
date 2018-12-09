from collections import defaultdict
import itertools as it


def parse_frequencies(filename: str) -> [int]:
    with open(filename) as frequency_changes:
        frequencies = map(lambda x: int(x[:-1]),
                          frequency_changes)
        frequencies_list = list(frequencies)
    return frequencies_list


def answer_function_part_one(filename: str) -> int:
    frequencies = parse_frequencies(filename)
    return sum(frequencies)


def answer_function_part_two(filename: str) -> int:
    def is_repeated(occurrences: defaultdict, frequency_change: int) -> bool:
        occurrences[frequency_change] += 1
        return occurrences[frequency_change] != 2

    occurrences = defaultdict(int)
    frequencies = parse_frequencies(filename)

    list(it.takewhile(lambda frequency: is_repeated(occurrences,
                                                    frequency),
                      it.accumulate(it.chain([0], it.cycle(frequencies)))))
    occurrences_inverted = {value: key for key, value in occurrences.items()}
    return occurrences_inverted[2]


if __name__ == '__main__':
    FILENAME = '../data/input.txt'
    answer_first = answer_function_part_one(FILENAME)
    answer_second = answer_function_part_two(FILENAME)

    print(f'First answer: {answer_first}')
    print(f'Second answer: {answer_second}')

