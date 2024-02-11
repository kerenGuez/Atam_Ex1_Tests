from itertools import combinations
from random import randint


MAX_NUM = 10_000
MIN_NUM = -10_000


def generate_n_numbers(n: int):
    return [randint(MIN_NUM, MAX_NUM) for _ in range(n)]


def all_subgroups(arr):
    subgroups = []
    arr_indexes = list(range(len(arr)))
    for r in range(1, (len(arr) + 1)):
        subgroup = list(combinations(arr_indexes, r))
        for group in subgroup:
            complement_index_group = [idx for idx in arr_indexes if idx not in group]
            num_group = [arr[idx] for idx in group]
            complement_group = [arr[idx] for idx in complement_index_group]
            group1 = [num_group, complement_group]
            if group1[::-1] not in subgroups:
                subgroups.append(group1)
    return subgroups


def is_strictly_dec(lis):
    return lis == sorted(set(lis))[::-1]


def is_strictly_inc(lis):
    return lis == sorted(set(lis))


def find_good_groups(arr):
    lists = all_subgroups(arr)
    good_groups = []
    for group in lists:
        if is_strictly_inc(group[0]):
            if is_strictly_dec(group[1]):
                good_groups.append([group[1], group[0]])
        if is_strictly_dec(group[0]):
            if is_strictly_inc(group[1]):
                good_groups.append([group[0], group[1]])
    return good_groups
