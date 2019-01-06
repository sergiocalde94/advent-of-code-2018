import re
import datetime
import functools as ft
import pandas as pd

REGEX_PARSE = r'\[\d+-(\d+-\d+ \d+:\d+)\] Guard #(\d+) (.*)'
REGEX_PARSE_NO_GUARD = r'\[\d+-(\d+-\d+ \d+:\d+)\] (.*)'


def parse_and_make_it_pandas_friendly(filename_input: str,
                                      filename_output: str) -> None:
    open_input = open(filename_input)
    open_output = open(filename_output, 'w')
    with open_input as file_input, open_output as file_output:
        file_output.write('date,guard_id,action\n')
        for line in file_input:
            match = re.match(REGEX_PARSE, line)
            if match:
                file_output.write(f'{match[1]},{match[2]},{match[3]}\n')
            else:
                match_no_guard = re.match(REGEX_PARSE_NO_GUARD, line)
                date, action = match_no_guard[1], match_no_guard[2]
                file_output.write(f'{date},,{action}\n')


def read_parsed_file(filename: str) -> pd.DataFrame:
    def date_parser(date_string: str) -> datetime.datetime:
        return pd.datetime.strptime(date_string, '%m-%d %H:%M')
    return pd.read_csv(filename, parse_dates=['date'], date_parser=date_parser)


def sorted_and_ffill_guards(df_log_guards: pd.DataFrame) -> pd.DataFrame:
    df_log_guards_copy = df_log_guards.copy()
    df_log_guards_copy = df_log_guards_copy.sort_values(by='date')
    df_falls_asleep_vs_wakes_up = pd.DataFrame(data=dict(
        date_falls_asleep=(df_log_guards_copy
                           .loc[df_log_guards_copy['action'] == 'falls asleep',
                                'date']
                           .values),
        date_wakes_up=(df_log_guards_copy
                       .loc[df_log_guards_copy['action'] == 'wakes up',
                            'date']
                       .values)))
    minutes_sleeping = (df_falls_asleep_vs_wakes_up
                        .apply(lambda x: pd.date_range(x['date_falls_asleep'],
                                                       x['date_wakes_up'],
                                                       freq='T',
                                                       closed='left'),
                               axis=1))
    df_minutes_sleeping = pd.DataFrame(data=dict(),
                                       index=ft.reduce(lambda a, b: a.union(b),
                                                       minutes_sleeping))
    df_log_guards_copy = df_log_guards_copy.set_index('date')
    df_log_guards_copy = (df_log_guards_copy
                          .loc[df_log_guards_copy['action'] != 'falls asleep'])
    df_log_guards_copy = (df_log_guards_copy.join(df_minutes_sleeping,
                                                  how='outer',
                                                  lsuffix='_guards',
                                                  rsuffix='_sleeping',
                                                  sort=True))
    df_log_guards_copy['guard_id'] = (df_log_guards_copy['guard_id']
                                      .ffill()
                                      .astype(int))
    df_log_guards_copy['action'] = (df_log_guards_copy['action']
                                    .fillna('sleeping'))

    return df_log_guards_copy


def get_minutes_sleeping_by_guard(
        df_log_guards_sorted: pd.DataFrame) -> pd.DataFrame:
    df_log_guards_sorted_copy = df_log_guards_sorted.copy()
    df_log_guards_sorted_copy['minute'] = (df_log_guards_sorted_copy
                                           .index
                                           .minute)
    minutes_sleeping_by_guard = (df_log_guards_sorted_copy
                                 .loc[df_log_guards_sorted_copy['action']
                                      == 'sleeping', :]
                                 .groupby(['guard_id', 'minute'])
                                 .count()
                                 .reset_index())
    columns_necessary = dict(guard_id='guard_id', minute='minute', action='times')
    minutes_sleeping_by_guard = minutes_sleeping_by_guard[list(
        columns_necessary.keys())]
    minutes_sleeping_by_guard.columns = columns_necessary.values()

    return minutes_sleeping_by_guard


def answer_function_part_one(filename_input: str, filename_output: str) -> int:
    parse_and_make_it_pandas_friendly(filename_input, filename_output)
    df_log_guards = read_parsed_file(filename_output)
    df_log_guards_sorted = sorted_and_ffill_guards(df_log_guards)
    df_minutes_sleeping_by_guard = get_minutes_sleeping_by_guard(
        df_log_guards_sorted)
    df_minutes_sleeping_by_guard_grouped = (df_minutes_sleeping_by_guard
                                            .groupby('guard_id')
                                            ['times']
                                            .sum()
                                            .reset_index())
    guard_id_most_minutes_asleep = (
        df_minutes_sleeping_by_guard_grouped
        .loc[df_minutes_sleeping_by_guard_grouped['times']
             == df_minutes_sleeping_by_guard_grouped['times'].max(),
             'guard_id']
        .iloc[0]
    )
    df_minutes_sleeping_most_guard = (
        df_minutes_sleeping_by_guard
        .loc[df_minutes_sleeping_by_guard['guard_id']
             == guard_id_most_minutes_asleep]
    )
    return (df_minutes_sleeping_most_guard
            .loc[df_minutes_sleeping_most_guard['times']
                 == df_minutes_sleeping_most_guard['times'].max(),
                 ['guard_id', 'minute']]
            .apply(lambda x: x['guard_id'] * x['minute'], axis=1)
            .iloc[0])


def answer_function_part_two(filename_input: str, filename_output: str) -> int:
    parse_and_make_it_pandas_friendly(filename_input, filename_output)
    df_log_guards = read_parsed_file(filename_output)
    df_log_guards_sorted = sorted_and_ffill_guards(df_log_guards)
    df_minutes_sleeping_by_guard = get_minutes_sleeping_by_guard(
        df_log_guards_sorted)

    return (df_minutes_sleeping_by_guard
            .loc[df_minutes_sleeping_by_guard['times']
                 == df_minutes_sleeping_by_guard['times'].max()]
            .apply(lambda x: x['guard_id'] * x['minute'], axis=1)
            .iloc[0])

if __name__ == '__main__':
    FILENAME_INPUT = '../data/input.txt'
    FILENAME_OUTPUT = '../data/input.csv'
    answer_first = answer_function_part_one(FILENAME_INPUT, FILENAME_OUTPUT)
    answer_second = answer_function_part_two(FILENAME_INPUT, FILENAME_OUTPUT)

    print(f'First answer: {answer_first}')
    print(f'Second answer: {answer_second}')
