import os
import sys
import math
from random import sample

from generate_const import (generate_valid_bin, generate_valid_oct, generate_valid_hex, generate_valid_dec,
                            generic_generate_invalid)


COLOR_END = "\033[0m"
COLOR_AQUA = "\033[96m"
COLOR_YELLOW = "\033[93m"
TMP_FILE_PATH = "tmp_file"


def generate_data_section(num_const: str):
    """Generates a random list of numbers and returns the data section."""
    data_section = f""".section .data
command: .ascii "movl ${num_const}, %eax"
integer: .long 0
legal: .byte 0"""
    return data_section


def generate_sample_file(data_section, integer, legal):
    sample_file = f""".global _start

.section .text

  mov $integer, %rax
  cmpl ${integer}, (%rax)
  jne bad_exit
  mov $legal, %rax
  cmpl ${legal}, (%rax)
  jne bad_exit


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


def basic_good_binary():
    return ["0b10"]   # Good binary


def basic_bad_binary():
    return ["0b2"]    # Bad binary


def basic_good_hex():
    return ["0xFA"]      # Hexadecimal


def basic_bad_hex():
    return ["0xF~"]    # Bad Hexadecimal


def basic_good_octal():
    return ["0760"]      # Octal


def basic_bad_octal():
    return ["08"]   # Bad Octal


def basic_good_decimal():
    return ["105", "0"]        # Decimal


def basic_bad_decimal():
    return ["", "1.05", "AB", ":"]     # Empty string


def write(tmp_file_path, content):
    with open(tmp_file_path, 'w') as file:
        file.write(content)


def create_tmp_file(integer, legal, num_const):
    data_section = generate_data_section(num_const)
    sample_file = generate_sample_file(data_section, integer, legal)
    write(TMP_FILE_PATH, sample_file)


def generic_run_test(asm_file, tests_file, integer, legal, num_const):
    try:
        create_tmp_file(integer=integer, legal=legal, num_const=num_const)
        os.system(f'./{tests_file} {asm_file} {TMP_FILE_PATH}')
        os.system(f'rm -f {TMP_FILE_PATH}')
    except Exception as e:
        os.system(f'rm -f {TMP_FILE_PATH}')
        raise e


def run_generic_tests(test_name, good_lis, bad_lis, asm_file, tests_file):
    print(f"{COLOR_YELLOW} --- Running Good {test_name} Tests --- {COLOR_END}{good_lis}")
    for num in good_lis:
        print(f"{COLOR_YELLOW} Testing:{COLOR_END}'{num}'")
        generic_run_test(asm_file=asm_file, tests_file=tests_file, integer=num, legal=1, num_const=num)

    print(f"{COLOR_YELLOW} --- Running Bad {test_name} Tests --- {COLOR_END}{bad_lis}")
    for num in bad_lis:
        print(f"{COLOR_YELLOW} Testing:{COLOR_END}'{num}'")
        generic_run_test(asm_file=asm_file, tests_file=tests_file, integer=0, legal=0, num_const=num)
    print()


def run_tests(asm_file,
              tests_file,
              test_name,
              good_basic_lis,
              bad_basic_lis,
              good_random_lis,
              bad_random_lis):
    """Runs a single test."""
    try:
        print(f"{COLOR_AQUA}--- Testing For {test_name} ---{COLOR_END}")
        # Basic Tests:
        run_generic_tests(test_name=f"Basic {test_name}", good_lis=good_basic_lis, bad_lis=bad_basic_lis,
                          asm_file=asm_file, tests_file=tests_file)

        # Randomized Tests:
        run_generic_tests(test_name=f"Randomized {test_name}", good_lis=good_random_lis, bad_lis=bad_random_lis,
                          asm_file=asm_file, tests_file=tests_file)

    except Exception as e:
        os.system(f'rm {TMP_FILE_PATH}')
        raise e


def run_all(asm_file, tests_file, generate_num: int = 10):
    # Binary
    good_basic_bin_lis, bad_basic_bin_lis = basic_good_binary(), basic_bad_binary()
    good_random_bin_lis = generate_valid_bin()
    bad_random_bin_lis = generic_generate_invalid(good_chars="01", generate_num=generate_num, prefix="0b")
    run_tests(asm_file=asm_file,
              tests_file=tests_file,
              test_name="Binary",
              good_basic_lis=good_basic_bin_lis, bad_basic_lis=bad_basic_bin_lis,
              good_random_lis=good_random_bin_lis, bad_random_lis=bad_random_bin_lis)
    # Octal
    good_basic_oct_lis, bad_basic_oct_lis = basic_good_octal(), basic_bad_octal()
    good_random_oct_lis = generate_valid_oct(generate_num=generate_num)
    bad_random_oct_lis = generic_generate_invalid(good_chars="01234567", generate_num=generate_num, prefix="0")
    run_tests(asm_file=asm_file,
              tests_file=tests_file,
              test_name="Octal",
              good_basic_lis=good_basic_oct_lis, bad_basic_lis=bad_basic_oct_lis,
              good_random_lis=good_random_oct_lis, bad_random_lis=bad_random_oct_lis)

    # Decimal
    good_basic_dec_lis, bad_basic_dec_lis = basic_good_decimal(), basic_bad_decimal()
    good_random_dec_lis = generate_valid_dec(generate_num=generate_num)
    bad_random_lis = generic_generate_invalid(good_chars="0123456789", generate_num=generate_num)
    bad_random_chosen = sample(bad_random_lis, math.ceil(generate_num / 2))
    bad_random_dec_lis = generic_generate_invalid(good_chars="0123456789", generate_num=generate_num, prefix="")
    bad_random_dec_chosen = sample(bad_random_dec_lis, math.ceil(generate_num / 2))
    bad_chosen_dec_lis = bad_random_chosen + bad_random_dec_chosen
    run_tests(asm_file=asm_file,
              tests_file=tests_file,
              test_name="Decimal",
              good_basic_lis=good_basic_dec_lis, bad_basic_lis=bad_basic_dec_lis,
              good_random_lis=good_random_dec_lis, bad_random_lis=bad_chosen_dec_lis)

    # Hexadecimal
    good_basic_hex_lis, bad_basic_hex_lis = basic_good_hex(), basic_bad_hex()
    good_random_hex_lis = generate_valid_hex(generate_num=generate_num)
    bad_random_hex_lis = generic_generate_invalid(good_chars="0123456789ABCDEF", generate_num=generate_num, prefix="0x")
    run_tests(asm_file=asm_file,
              tests_file=tests_file,
              test_name="Hexadecimal",
              good_basic_lis=good_basic_hex_lis, bad_basic_lis=bad_basic_hex_lis,
              good_random_lis=good_random_hex_lis, bad_random_lis=bad_random_hex_lis)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    the_asm_file = arguments[0]
    the_tests_file = arguments[1]
    if len(arguments) < 2:
        print('Usage: python3 py_tests_ex_5.py <asm_file> <tests_file> (?generate_num)')
        sys.exit(1)

    if len(arguments) >= 3:
        the_generate_num = int(arguments[2])
    else:
        the_generate_num = 10

    run_all(asm_file=the_asm_file, tests_file=the_tests_file, generate_num=the_generate_num)
