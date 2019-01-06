import collections

import numpy as np

Position = collections.namedtuple('Position', ['id', 'x', 'y'])


def parse_squares(filename: str) -> [int]:
    with open(filename) as positions:
        positions_parsed = map(lambda x: x.replace(',', '').split(), positions)
        positions_matched = [Position(chr(65 + index), *map(int, match))
                             for index, match in enumerate(positions_parsed)]
    return positions_matched


def fill_min_and_max(position: Position, attr: str,
                     current_min: int, current_max: int) -> (int, int):
    position_value = getattr(position, attr)
    if position_value > current_max:
        current_max = position_value
    if position_value < current_min:
        current_min = position_value
    return current_min, current_max


def get_min_and_max(positions: [Position]) -> (int, int, int, int):
    min_x, min_y, max_x, max_y = np.inf, np.inf, -np.inf, -np.inf
    for position in positions:
        min_x, max_x = fill_min_and_max(position, 'x', min_x, max_x)
        min_y, max_y = fill_min_and_max(position, 'y', min_y, max_y)
    return min_x, min_y, max_x, max_y


def rescale_positions(positions: [Position],
                      min_x: int, min_y: int) -> [Position]:
    return [Position(position.id, position.x - min_x, position.y - min_y)
            for position in positions]


def fill_board(board: np.array, positions: [Position]) -> np.array:
    board_copy = board.copy()
    for position in positions:
        board_copy[position.x, position.y] = position.id
    return board_copy


def get_manhattan_distance_dict(
        board: np.array,
        positions: [Position],
        ignore_filled_positions: bool = True) -> collections.defaultdict:
    manhattan_distance_dict = collections.defaultdict(list)
    for index, value in np.ndenumerate(board):
        if not value or not ignore_filled_positions:
            for position in positions:
                manhattan_distance_dict[index].append(
                    dict(
                        id=position.id,
                        distance=(abs(index[0] - position.x)
                                  + abs(index[1] - position.y))
                    )
                )
    return manhattan_distance_dict


def fill_board_manhattan_distance(
        board: np.array,
        manhattan_distance_dict: collections.defaultdict) -> np.array:
    board_copy = board.copy()
    for index, distances in manhattan_distance_dict.items():
        min_distance = min(distances, key=lambda x: x['distance'])
        board_copy[index] = (min_distance['id']
                             if len([distance
                                     for distance in distances
                                     if (distance['distance']
                                         == min_distance['distance'])]) == 1
                             else '')
    return board_copy


def get_corners_id(board: np.array, shape: (int, int)) -> [str]:
    return [board[0, 0], board[0, shape[1] - 1],
            board[shape[0] - 1, 0], board[shape[0] - 1, shape[1] - 1]]


def count_areas(board: np.array) -> zip:
    item_id, count = np.unique(board, return_counts=True)
    return zip(item_id, count)


def fill_board_manhattan_distance_less_than(
        board: np.array,
        maximum: int,
        manhattan_distance_dict: collections.defaultdict) -> np.array:
    board_copy = board.copy()
    for index, distances in manhattan_distance_dict.items():
        sum_distances = sum(map(lambda x: x['distance'], distances))
        board_copy[index] = (1
                             if sum_distances < maximum
                             else 0)
    return board_copy


def answer_function_part_one(filename: str) -> int:
    positions = parse_squares(filename)
    min_x, min_y, max_x, max_y = get_min_and_max(positions)
    positions_rescaled = rescale_positions(positions, min_x, min_y)
    shape_x, shape_y = max_x - min_x + 1, max_y - min_y + 1
    board = np.empty((shape_x, shape_y), dtype=str)
    board_filled = fill_board(board, positions_rescaled)
    manhattan_distance_dict = get_manhattan_distance_dict(board_filled,
                                                          positions_rescaled)
    board_filled_manhattan = fill_board_manhattan_distance(
        board_filled,
        manhattan_distance_dict
    )
    empty_and_corners = ['',
                         *get_corners_id(
                             board_filled_manhattan, (shape_x, shape_y))]
    all_areas = count_areas(board_filled_manhattan)
    all_areas_filtered = filter(lambda x: x[0] not in empty_and_corners,
                                all_areas)
    return max(map(lambda x: x[1], all_areas_filtered))


def answer_function_part_two(filename: str, maximum: int) -> int:
    positions = parse_squares(filename)
    min_x, min_y, max_x, max_y = get_min_and_max(positions)
    positions_rescaled = rescale_positions(positions, min_x, min_y)
    shape_x, shape_y = max_x - min_x + 1, max_y - min_y + 1
    board = np.empty((shape_x, shape_y), dtype=str)
    board_filled = fill_board(board, positions_rescaled)
    manhattan_distance_dict = get_manhattan_distance_dict(board_filled,
                                                          positions_rescaled,
                                                          False)
    board_filled_manhattan_distance_mask = (
        fill_board_manhattan_distance_less_than(board_filled,
                                                maximum,
                                                manhattan_distance_dict)
    )
    return (board_filled_manhattan_distance_mask == '1').sum()


if __name__ == '__main__':
    FILENAME = '../data/input.txt'
    answer_first = answer_function_part_one(FILENAME)
    answer_second = answer_function_part_two(FILENAME, 10000)

    print(f'First answer: {answer_first}')
    print(f'Second answer: {answer_second}')
