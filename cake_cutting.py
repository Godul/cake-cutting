from math import log10


PRECISION = 0.000001
DECIMAL_PLACES = int(log10(1 / PRECISION))


def validate_preference(pref: dict) -> bool:
    sorted_intervals = list(sorted(pref.keys()))

    if not sorted_intervals:
        return False

    if sorted_intervals[0][0] != 0:
        return False

    if sorted_intervals[-1][1] != 1:
        return False

    for i_1, i_2 in zip(sorted_intervals, sorted_intervals[1:]):
        if i_1[1] < i_2[0]:
            return False

    return True


def communicate_with_user() -> list:
    print('Please enter number of players.')
    players_n = int(input())
    prefs = []

    for player in range(players_n):
        pref = {}

        print(f'PLAYER {player}:')

        while not validate_preference(pref):
            print(f'Please enter preference of interval from [0, 1]. You need to cover it all.')
            print("Format: left right value")

            x, y, z = map(float, input().split())
            pref[(x, y)] = z
        prefs.append(pref)

    return prefs


def get_valuation(a, b, pref):
    result = 0.

    for (x, y), z in list(sorted(pref.items())):
        if a <= x and y <= b:
            result += z
            continue

        if x < a < y <= b or a <= x < b < y or (x < a and b < y):
            result += z * (b - a) / (y - x)

    return result


def calculate_division_point(left: float, expected_value: float, pref: dict):
    right = 1.
    valuation = get_valuation(left, right, pref)

    while abs(valuation - expected_value) > PRECISION:
        if valuation > expected_value:
            right = (left + right) / 2
        else:
            right = (1. + right) / 2

        valuation = get_valuation(left, right, pref)

    return right


def calculate_division_points(left: float, players_left: set, prefs: list) -> list:
    result = []
    expected_value = (1 - left) / len(players_left)

    for player in players_left:
        pref = prefs[player]
        result.append((calculate_division_point(left, expected_value, pref), player))
    return result


def calculate_division(prefs: list):
    division = {}
    players_left = set(range(len(prefs)))
    current_point = 0.

    while len(players_left) > 1:
        div_point, player_to_remove = sorted(calculate_division_points(current_point, players_left, prefs))[0]
        division[player_to_remove] = (current_point, div_point)
        players_left.remove(player_to_remove)
        current_point = div_point

    division[next(iter(players_left))] = (current_point, 1.)
    return division


def print_result(division):
    print('Result:')
    for player, interval in division.items():
        print(f'PLAYER {player} -> [{round(interval[0], DECIMAL_PLACES)}, {round(interval[1], DECIMAL_PLACES)}]')


def main():
    prefs = communicate_with_user()
    division = calculate_division(prefs)
    print_result(division)


if __name__ == '__main__':
    main()
