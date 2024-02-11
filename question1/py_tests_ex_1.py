import os
import sys


def mapping_table(include_symbols=False):
    symbol_mapping = {'1': '!',
                      '2': '@',
                      '3': '#',
                      '4': '$',
                      '5': '%',
                      '6': '^',
                      '7': '&',
                      '8': '*',
                      '9': '(',
                      '0': ')',
                      '`': '~',
                      '-': '_',
                      '=': '+',
                      '[': '{',
                      ']': '}',
                      ';': ':',
                      "'": '"',
                      '\\': '|',
                      ',': '<',
                      '.': '>',
                      '/': '?',
                      '!': '!',
                      '@': '@',
                      '#': '#',
                      '$': '$',
                      '%': '%',
                      '^': '^',
                      '&': '&',
                      '*': '*',
                      '(': '(',
                      ')': ')',
                      '~': '~',
                      '_': '_',
                      '+': '+',
                      '{': '{',
                      '}': '}',
                      ':': ':',
                      '"': '"',
                      '|': '|',
                      '<': '<',
                      '>': '>',
                      '?': '?'
                      }
    letter_mapping = {'a': 'A',
                      'b': 'B',
                      'c': 'C',
                      'd': 'D',
                      'e': 'E',
                      'f': 'F',
                      'g': 'G',
                      'h': 'H',
                      'i': 'I',
                      'j': 'J',
                      'k': 'K',
                      'l': 'L',
                      'm': 'M',
                      'n': 'N',
                      'o': 'O',
                      'p': 'P',
                      'q': 'Q',
                      'r': 'R',
                      's': 'S',
                      't': 'T',
                      'u': 'U',
                      'v': 'V',
                      'w': 'W',
                      'x': 'X',
                      'y': 'Y',
                      'z': 'Z',
                      'A': 'A',
                      'B': 'B',
                      'C': 'C',
                      'D': 'D',
                      'E': 'E',
                      'F': 'F',
                      'G': 'G',
                      'H': 'H',
                      'I': 'I',
                      'J': 'J',
                      'K': 'K',
                      'L': 'L',
                      'M': 'M',
                      'N': 'N',
                      'O': 'O',
                      'P': 'P',
                      'Q': 'Q',
                      'R': 'R',
                      'S': 'S',
                      'T': 'T',
                      'U': 'U',
                      'V': 'V',
                      'W': 'W',
                      'X': 'X',
                      'Y': 'Y',
                      'Z': 'Z'}
    bad_symbols = {
        ' ': '0xff',
        '\n': '0xff',
        '\t': '0xff',
        '\r': '0xff',
        '\x0b': '0xff',
        '\x0c': '0xff'
    }
    return {**symbol_mapping, **letter_mapping, **bad_symbols} if include_symbols else {**letter_mapping, **bad_symbols}


def update_file(sample_path, new_character, new_mapped, old_character=97, old_mapped=65):
    """Updates the file with the new character to check along with its mapped value."""
    replace_character = fr'sed -i "s/character: .byte {old_character}/character: .byte {new_character}/" {sample_path}'
    replace_mapped_value = fr' sed -i "s/cmpl \${old_mapped}, (%rax)/cmpl \${new_mapped}, (%rax)/" {sample_path}'
    os.system(replace_character)
    os.system(replace_mapped_value)


def run_tests(sample_path, asm_file, tests_file, include_symbols=False):
    my_mapping_table = mapping_table(include_symbols)
    for character, mapped_value in my_mapping_table.items():
        # Override the file with the new character and its mapped value to check
        mapped_value = ord(mapped_value) if mapped_value != '0xff' else '0xff'
        update_file(sample_path, ord(character), mapped_value)

        # Run the tests
        print(f"\033[93m --- Checking {character} -> {chr(mapped_value) if mapped_value != '0xff' else mapped_value}"
              f" conversion --- \033[0m")
        os.system(f'./{tests_file} {asm_file} {sample_path}')

        # CleanUp
        update_file(sample_path,
                    new_character=97,
                    new_mapped=65,
                    old_character=ord(character),
                    old_mapped=mapped_value)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    the_sample_path = arguments[0]
    the_asm_file = arguments[1]
    the_tests_file = arguments[2]
    the_include_symbols = False
    if len(arguments) < 3:
        print('Usage: python3 py_tests_ex_1.py <sample_tests_file_path> <asm_file> <tests_file> '
              '<the_include_symbols=False>')
        sys.exit(1)

    if len(arguments) >= 4:
        the_include_symbols = bool(arguments[3])

    run_tests(the_sample_path, the_asm_file, the_tests_file, the_include_symbols)
