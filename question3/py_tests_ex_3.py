import os
import sys
import subprocess
from random import randint
from find_inc_and_dec import find_good_groups, generate_n_numbers


COLOR_END = "\033[0m"
COLOR_AQUA = "\033[96m"
COLOR_YELLOW = "\033[93m"
TMP_FILE_PATH = "tmp_file"


def generate_data_section(nums: list):
    """Generates a random list of numbers and returns the data section."""
    arr_str = str(nums).replace('[', '').replace(']', '')
    size = len(nums)
    zeros = str([0] * size).replace('[', '').replace(']', '')

    data_section = f""".section .data
size:   .long {size}
source_array:   .long {arr_str}
up_array:   .long {zeros}
down_array:   .long {zeros}
bool:  .byte 0"""
    return data_section


def generate_array_check(up_arr, down_arr):
    """Generates the array check section."""
    array_check = ""
    for i, num in enumerate(up_arr):
        array_check += f"""
  up_idx_{i}:
  movl ${i}, %esi  # i = {i}
  movl (%r9d, %esi, 4), %eax  # eax = up_array[{i}]
  cmpl ${num}, %eax  # if up_array[{i}] != {num} then exit
  jne bad_exit
  
  """

    for j, num in enumerate(down_arr):
        array_check += f"""
  down_idx_{j}:
  movl ${j}, %r11d  # j = {j}
  movl (%r8d, %r11d, 4), %edx  # edx = down_array[{j}]
  cmpl ${num}, %edx  # if down_array[{j}] != {num} then exit
  jne bad_exit
      
      """

    return array_check


def generate_sample_file(array_check, data_section, result):
    sample_file = f""".global _start

.section .text

  mov $bool, %rax
  cmpl ${result}, (%rax)
  jne bad_exit

  movq $(up_array), %r9  # r9 = up_array(pointer)
  movq $(down_array), %r8  # r8 = down_array(pointer)
  xorl $0, %esi  # i = 0  (up array index)
  xorl $0, %r11d  # j = 0  (down array index)

  {array_check}

  movq $60, %rax
  movq $0, %rdi
  syscall

bad_exit:
  movq $60, %rax
  movq $1, %rdi
  syscall

{data_section}
"""

    return sample_file


def basic_tests():
    basic_test_able = [1, -2, 3, -4]
    basic_test_able4 = [-8862, 4749, -1224, -6827, 6405, -3307, -3307, 7584]
    basic_test_able2 = [-2592, -2024, 812, 4807]
    basic_test_able3 = [7922, 2612, -2961, 4354, 1689, 1204, -4607]
    basic_test_not_able = [1, 5, -3, -1]
    basic_empty = []
    return [basic_test_able, basic_test_able2, basic_test_able3, basic_test_able4, basic_empty, basic_test_not_able]


def write(tmp_file_path, content):
    with open(tmp_file_path, 'w') as file:
        file.write(content)


def run_single_test(asm_file, tests_file, test_arr):
    """Runs a single test."""
    try:
        print(f"{COLOR_YELLOW}Testing with: {COLOR_END}{test_arr}")
        good_groups = find_good_groups(test_arr)
        print(f"{COLOR_YELLOW}Good groups: {COLOR_END}{good_groups}")
        return_code = 1
        data_section = generate_data_section(test_arr)
        # Check if the array cannot be split into a strictly increasing and a strictly decreasing array
        if not len(good_groups) or not len(test_arr):
            result = 1 if not len(test_arr) else 0
            sample_file = generate_sample_file(array_check="", data_section=data_section, result=result)
            # Create the sample file
            write(TMP_FILE_PATH, sample_file)
            # Run the tests
            os.system(f'./{tests_file} {asm_file} {TMP_FILE_PATH}')

        else:

            # If the array can be split, check if assembly code can find at least one good split
            result = 1 if len(good_groups) else 0
            for group in good_groups:
                down_arr = group[0] + ([0] * (len(test_arr) - len(group[0])))
                up_arr = group[1] + ([0] * (len(test_arr) - len(group[1])))
                array_check = generate_array_check(up_arr, down_arr)
                sample_file = generate_sample_file(array_check=array_check, data_section=data_section, result=result)

                # Create the sample file
                write(TMP_FILE_PATH, sample_file)

                # Run the tests
                command = ['./' + tests_file, asm_file, TMP_FILE_PATH]
                command_result = subprocess.run(command, stdout=subprocess.PIPE)
                return_code = command_result.returncode

                # We need at least one good split
                if return_code == 0:
                    print(f"${asm_file} tested with ${TMP_FILE_PATH}: \033[32mPASS\033[0m")
                    break

            # If no good split was found, print FAIL
            if return_code != 0:
                print(f"${asm_file} tested with ${TMP_FILE_PATH}: \033[31mFAIL\033[0m")

        print()
    except Exception as e:
        os.system(f'rm {TMP_FILE_PATH}')
        raise e
    else:
        os.system(f'rm {TMP_FILE_PATH}')


if __name__ == '__main__':
    arguments = sys.argv[1:]
    the_asm_file = arguments[0]
    the_tests_file = arguments[1]
    if len(arguments) < 2:
        print('Usage: python3 py_tests_ex_3.py <asm_file> <tests_file> (?generate_num)')
        sys.exit(1)

    if len(arguments) >= 3:
        the_generate_num = int(arguments[2])
    else:
        the_generate_num = 10

    print(f"{COLOR_AQUA}--- Running Basic Tests ---{COLOR_END}")
    basics = basic_tests()
    for basic in basics:
        run_single_test(asm_file=the_asm_file, tests_file=the_tests_file, test_arr=basic)

    print(f"{COLOR_AQUA}--- Running Randomized Tests ---{COLOR_END}")
    for _ in range(the_generate_num):
        amount_of_numbers = randint(0, 10)
        the_test_arr = generate_n_numbers(amount_of_numbers)
        run_single_test(asm_file=the_asm_file, tests_file=the_tests_file, test_arr=the_test_arr)
