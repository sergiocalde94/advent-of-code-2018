import re
import collections
import numpy as np
import itertools as it
import functools as ft

Position = collections.namedtuple('Position',
                                  ['id', 'x', 'y', 'width', 'height'])
REGEX_PARSE = r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'


def get_square_positions(positions: [Position]) -> [zip]:
    return [list(it.product(range(position.x, position.x + position.width),
                            range(position.y, position.y + position.height)))
            for position in positions]


def get_squares_shape(positions: [Position]) -> (int, int):
    max_x = max([position.x + position.width for position in positions])
    max_y = max([position.y + position.height for position in positions])

    return max_x + 1, max_y + 1


def parse_squares(filename: str) -> [int]:
    with open(filename) as positions:
        positions_match = map(lambda x: re.match(REGEX_PARSE, x), positions)
        positions_match_list = [Position(*(int(match[i]) for i in range(1, 6)))
                                for match in positions_match]
    return positions_match_list


def fill_board(board: np.array, square_positions: [(int, int)]) -> np.array:
    board_copy = board.copy()
    for square_position in square_positions:
        for position_x, position_y in square_position:
            board_copy[position_x, position_y] += 1
    return board_copy


def id_no_overlap(board: np.array, square_positions: [(int, int)]) -> int:
    def no_overlap_in_position(position: (int, int), board: np.array) -> bool:
        return board[position[0], position[1]] == 1
    no_overlap_in_position_current_board = ft.partial(no_overlap_in_position,
                                                      board=board)

    for index, square_position in enumerate(square_positions):
        square_position_filtered = filter(no_overlap_in_position_current_board,
                                          square_position)
        if len(square_position) == sum(1 for _ in square_position_filtered):
            return index + 1
    else:
        return -1


def answer_function_part_one(filename: str) -> int:
    positions_match = parse_squares(filename)
    square_positions = get_square_positions(positions_match)
    shape_x, shape_y = get_squares_shape(positions_match)
    board = np.zeros((shape_x, shape_y))
    board_filled = fill_board(board, square_positions)

    return (board_filled >= 2).sum()


def answer_function_part_two(filename: str) -> int:
    positions_match = parse_squares(filename)
    square_positions = get_square_positions(positions_match)
    shape_x, shape_y = get_squares_shape(positions_match)
    board = np.zeros((shape_x, shape_y))
    board_filled = fill_board(board, square_positions)
    return id_no_overlap(board_filled, square_positions)


if __name__ == '__main__':
    FILENAME = '../data/input.txt'
    answer_first = answer_function_part_one(FILENAME)
    answer_second = answer_function_part_two(FILENAME)

    print(f'First answer: {answer_first}')
    print(f'Second answer: {answer_second}')

