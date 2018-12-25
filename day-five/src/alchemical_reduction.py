def read_polymer_from_file(filename: str) -> str:
    with open(filename) as file:
        return file.read().replace('\n', '')


def reduce_polymer(polymer: str) -> str:
    possibilities = {f'{unit}{unit.upper()}'
                     for unit in set(polymer.lower())}
    possibilities = possibilities.union({i[::-1] for i in possibilities})

    for possibility in possibilities:
        polymer = polymer.replace(possibility, '')
    return polymer


def reduce_polymer_until_convergence(polymer: str) -> str:
    while True:
        new_polymer = reduce_polymer(polymer)
        if new_polymer == polymer:
            break
        else:
            polymer = new_polymer
    return polymer


def answer_function_part_one(filename: str) -> int:
    polymer = read_polymer_from_file(filename)
    polymer = reduce_polymer_until_convergence(polymer)
    return len(polymer)


def answer_function_part_two(filename: str) -> int:
    polymer = read_polymer_from_file(filename)
    set(polymer.lower())
    polymers = [polymer.replace(unit, '').replace(unit.upper(), '')
                for unit in set(polymer.lower())]
    return min(map(lambda x: len(reduce_polymer_until_convergence(x)),
                   polymers))


if __name__ == '__main__':
    FILENAME = '../data/input.txt'
    answer_first = answer_function_part_one(FILENAME)
    answer_second = answer_function_part_two(FILENAME)

    print(f'First answer: {answer_first}')
    print(f'Second answer: {answer_second}')
