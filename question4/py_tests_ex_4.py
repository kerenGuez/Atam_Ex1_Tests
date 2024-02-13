import os
import sys
import string
from math import ceil
from random import randint

from increasing_series import (generate_strictly_increasing,
                               generate_increasing,
                               generate_semi_increasing,
                               generate_decreasing,
                               generate_more_than_1_bad,
                               print_list,
                               MAX_LIST_LEN)

COLOR_END = "\033[0m"
COLOR_RED = "\033[91m"
COLOR_AQUA = "\033[96m"
COLOR_YELLOW = "\033[93m"
tmp_file_path = "tmp_file.txt"


def new_data_section(nums_list: list):
    """Returns the pattern of the linked list.
    Example:
        .section .data
        D: .quad 4
        .quad 0
        C: .quad 3
        .quad D
        B: .quad 2
        .quad C
        A: .quad 1
        .quad B
        head: .quad A
        result: .byte 3
    """
    pattern = ""
    upper_chars = string.ascii_uppercase
    if not len(nums_list):
        return "\n.section .data\nhead: .quad 0\nresult: .byte 0\n"

    for idx, num in enumerate(nums_list):
        pattern = (f"{upper_chars[idx]}: .quad {nums_list[idx]}\n" +
                   f".quad {upper_chars[idx + 1] if idx < len(nums_list) - 1 else 0}\n" + pattern)

    pattern += "head: .quad A\n"
    return "\n.section .data\n" + pattern + f"result: .byte 0\n"


def update_file(sample_path, new_result, new_list_pattern=None, revert=False):
    """Update the file with the new data section and necessary result to check."""
    replace_mapped_value = fr' sed -i "s/cmpl \$3, (%rax)/cmpl \${new_result}, (%rax)/" {tmp_file_path}'
    os.system(replace_mapped_value)
    if revert:
        os.system(f'cp {sample_path} {tmp_file_path}')
    else:
        add_data_section = fr'echo "{new_list_pattern}" >> {tmp_file_path}'
        os.system(add_data_section)


def basic_strictly_increasing():
    return [[], [1], [1, 2, 3, 4]]


def run_single_test(sample_path, asm_file, tests_file, new_list, new_result):
    """Runs a single test."""
    new_list_pattern = new_data_section(new_list)
    update_file(sample_path=sample_path,
                new_result=new_result,
                new_list_pattern=new_list_pattern)
    os.system(f'./{tests_file} {asm_file} {tmp_file_path}')
    update_file(sample_path=sample_path,
                new_result=3,
                revert=True)


def generic_test(sample_path,
                 asm_file,
                 tests_file,
                 test_name,
                 result,
                 basic_tests_func,
                 generate_func,
                 list_size=None,
                 generate_num=10):
    """Generic test for semi-increasing and decreasing linked lists."""
    print(f"{COLOR_AQUA}--- Testing {test_name} Linked lists ---{COLOR_END}")
    basic_lists = basic_tests_func()
    new_result = result

    print(f"{COLOR_YELLOW} --- Running {test_name} Basic Tests --- {COLOR_END}")
    for lis in basic_lists:
        print(f"Testing list: ", end="")
        print_list(lis)
        run_single_test(sample_path, asm_file, tests_file, lis, new_result)
        print()

    if test_name == "More Than 1 Bad":
        generated_lists = []
        for i in range(generate_num):
            list_size = min(randint(3, MAX_LIST_LEN), MAX_LIST_LEN) if list_size is None else min(list_size,
                                                                                                  MAX_LIST_LEN)
            half_size = ceil(list_size / 2)
            num_bad = randint(2, half_size)
            generated_lists.append(generate_func(num_bad=num_bad, list_size=list_size))

    else:
        list_size = None if list_size is None else min(list_size, MAX_LIST_LEN)
        generated_lists = [generate_func(list_size=list_size) for _ in range(generate_num)]

    print(f"{COLOR_YELLOW} --- Running {test_name} Randomized Tests --- {COLOR_END}")
    for lis in generated_lists:
        print(f"Testing list: ", end="")
        print_list(lis)
        run_single_test(sample_path, asm_file, tests_file, lis, new_result)
        print()


def test_strictly_increasing(sample_path, asm_file, tests_file, generate_num=10):
    """Test that strictly increasing linked lists return 3."""
    generic_test(sample_path=sample_path,
                 asm_file=asm_file,
                 tests_file=tests_file,
                 test_name="Strictly Increasing",
                 result=3,
                 basic_tests_func=basic_strictly_increasing,
                 generate_func=generate_strictly_increasing,
                 generate_num=generate_num)


def basic_increasing():
    return [[1, 2, 2, 4], [1, 1, 3, 4], [4, 4, 4, 4], [1, 2, 4, 4], [1, 1, 1, 4]]


def test_increasing(sample_path, asm_file, tests_file, generate_num=10):
    """Test that increasing linked lists return 2."""
    generic_test(sample_path=sample_path,
                 asm_file=asm_file,
                 tests_file=tests_file,
                 test_name="Increasing",
                 result=2,
                 basic_tests_func=basic_increasing,
                 generate_func=generate_increasing,
                 generate_num=generate_num)


def basic_semi_increasing():
    return [5, 1, 2, 3], [1, 0, 3, 4], [1, 2, 0, 4], [1, 2, 3, 0], [4, 4, 4, 1]


def test_semi_increasing(sample_path, asm_file, tests_file, generate_num=10):
    """Test that semi-increasing linked lists return 1."""
    generic_test(sample_path=sample_path,
                 asm_file=asm_file,
                 tests_file=tests_file,
                 test_name="Semi-Increasing",
                 result=1,
                 basic_tests_func=basic_semi_increasing,
                 generate_func=generate_semi_increasing,
                 generate_num=generate_num)


def basic_decreasing():
    return [[4, 3, 2, 1], [4, 4, 3, 1], [4, 3, 3, 1], [4, 3, 2, 2]]


def test_decreasing(sample_path, asm_file, tests_file, generate_num=10):
    """Test that decreasing linked lists return 0."""
    generic_test(sample_path=sample_path,
                 asm_file=asm_file,
                 tests_file=tests_file,
                 test_name="Decreasing",
                 result=0,
                 basic_tests_func=basic_decreasing,
                 generate_func=generate_decreasing,
                 generate_num=generate_num)


def basic_more_than_1_bad():
    return [[5, 1, 0, 3], [5, 3, 2, 4], [4, 2, 1, 4], [4, 3, 2, 1], [5, 4, 4, 0]]


def test_more_than_1_bad(sample_path, asm_file, tests_file, generate_num=10):
    """Test that linked lists with more than 1 bad value return 0."""
    generic_test(sample_path=sample_path,
                 asm_file=asm_file,
                 tests_file=tests_file,
                 test_name="More Than 1 Bad",
                 result=0,
                 basic_tests_func=basic_more_than_1_bad,
                 generate_func=generate_more_than_1_bad,
                 generate_num=generate_num)


def run_all_tests(sample_path, asm_file, tests_file, generate_num=10):
    test_strictly_increasing(sample_path, asm_file, tests_file, generate_num)
    test_increasing(sample_path, asm_file, tests_file, generate_num)
    test_semi_increasing(sample_path, asm_file, tests_file, generate_num)
    test_decreasing(sample_path, asm_file, tests_file, generate_num)
    test_more_than_1_bad(sample_path, asm_file, tests_file, generate_num)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    the_sample_path = arguments[0]
    the_asm_file = arguments[1]
    the_tests_file = arguments[2]
    if len(arguments) < 3:
        print('Usage: python3 py_tests_ex_4.py <sample_tests_file_path> <asm_file> <tests_file> (?generate_num) ')
        sys.exit(1)

    if len(arguments) >= 4:
        the_generate_num = int(arguments[3])
    else:
        the_generate_num = 10

    os.system(f'cp {the_sample_path} {tmp_file_path}')
    run_all_tests(the_sample_path, the_asm_file, the_tests_file, generate_num=the_generate_num)

    # run_all_tests(the_sample_path, the_asm_file, the_tests_file)
    os.system(f'rm {tmp_file_path}')
