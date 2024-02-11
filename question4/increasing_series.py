from random import randint, sample


MAX_NUM = 10_000
MIN_NUM = 0
MAX_LIST_LEN = 26
RED = "\033[91m"
Orange = "\033[33m"
END = "\033[0m"


def generate_n_numbers(n: int):
    nums_lis = []
    while n:
        num = randint(MIN_NUM, MAX_NUM)
        if num not in nums_lis:
            nums_lis.append(num)
            n -= 1

    return nums_lis


def generate_strictly_increasing(list_size: int = None):
    """Generates a strictly increasing list. An increasing list that has no repeating numbers."""
    lis_size = min(randint(0, MAX_LIST_LEN) if not list_size else list_size, MAX_LIST_LEN)
    nums_lis = generate_n_numbers(lis_size)
    nums_lis.sort()
    return nums_lis


def generate_increasing(num_repeating: int = 1, random_num_repeating: bool = True, list_size: int = None):
    """Generates an increasing list with repeating numbers."""
    lis_size = min(randint(2, MAX_LIST_LEN) if not list_size else list_size, MAX_LIST_LEN)
    num_repeating = num_repeating if not random_num_repeating else max(1, int(lis_size / 2))
    nums_lis = generate_n_numbers((lis_size + 1) - num_repeating)
    final_list = []
    choose_repeating_nums = sample(nums_lis, min(num_repeating, len(nums_lis)))
    non_repeating = [num for num in nums_lis if num not in choose_repeating_nums]
    repetition_choice = lis_size - (num_repeating * 2)

    # Adding the repeating numbers
    for num in choose_repeating_nums:
        # number of times a number will repeat
        repetition = randint(2, max(2, repetition_choice))        # How much choice for repetition I have for next time
        repetition_choice = max(0, repetition_choice - repetition)
        final_list.extend([num] * repetition)

    repeating_len = len(final_list)
    final_list.extend(non_repeating[:(lis_size - repeating_len)])
    final_list.sort()

    return final_list


def generate_uniq(low: int, high: int, lis: list):
    """Generates a random number that is not in the given list."""
    rand = randint(low, high)
    while rand in lis:
        rand = randint(low, high)

    return rand


def plant_bad_value(lis: list, bad_index: int):
    if bad_index == 0:
        next_value = lis[bad_index + 1]
        bad_value = generate_uniq(next_value + 1, MAX_NUM, lis)  # previous value > next value

    else:
        previous_value = lis[bad_index - 1]
        bad_value = generate_uniq(MIN_NUM, previous_value - 1, lis)

    lis[bad_index] = bad_value
    return lis


def generate_inc_or_strict_inc(lis_size: int):
    is_strict_inc = randint(0, 1)
    increasing_list = generate_strictly_increasing(list_size=lis_size) if is_strict_inc \
        else generate_increasing(list_size=lis_size)
    return increasing_list


def generate_semi_increasing(bad_index: int = None, list_size: int = None):
    """Generates a semi-increasing list. A list that is increasing but has a single element that is not in order."""
    # Generate a strictly increasing list/a regular increasing list
    if bad_index is None:
        lis_size = min(randint(2, MAX_LIST_LEN) if not list_size else list_size, MAX_LIST_LEN)
        bad_index = randint(0, lis_size - 1)
    else:
        lis_size = min(randint(max(bad_index + 1, 2), MAX_LIST_LEN) if not list_size else list_size, MAX_LIST_LEN)

    increasing_list = generate_inc_or_strict_inc(lis_size)

    # Generate a random index to change the list to semi-increasing
    increasing_list = plant_bad_value(increasing_list, bad_index)
    return increasing_list


def generate_decreasing(list_size: int = None):
    """Generates a decreasing list. A list that is strictly decreasing."""
    lis_size = min(randint(3, MAX_LIST_LEN) if not list_size else list_size, MAX_LIST_LEN)
    nums_lis = generate_n_numbers(lis_size)
    nums_lis.sort(reverse=True)
    return nums_lis


def generate_more_than_1_bad(num_bad: int = 2, list_size: int = None):
    """Generates a decreasing list. A list that is strictly decreasing."""
    lis_size = min(randint(3, MAX_LIST_LEN) if list_size is None else list_size, MAX_LIST_LEN)
    increasing_list = generate_inc_or_strict_inc(lis_size)
    possible_indexes = list(range(lis_size))[::2]
    bad_indexes = sample(possible_indexes, min(num_bad, len(possible_indexes)))
    for bad_index in bad_indexes:
        increasing_list = plant_bad_value(increasing_list, bad_index)
    return increasing_list


def print_list(lis: list, color: str = END, indexes: list = None):
    """Prints the list and color the given indexes in red."""
    if len(lis) > 1 and indexes:
        end = ", "
        print("[", end='')
        for i, num in enumerate(lis):
            if i == len(lis) - 1:
                end = ""
            if i in indexes:
                print(f"{color}{num}{END}", end=end)
            else:
                print(f"{num}", end=end)
        print("]", end='')
    else:
        print(str(lis))
