from string import printable
from itertools import permutations
from random import randint, sample


def generate_valid_bin():
    """Generates a valid binary number."""
    valid_binaries_1 = ["0b0", "0b1"]
    valid_binaries_2 = ["0b00", "0b01", "0b10", "0b11"]
    valid_binaries_3 = ["0b000", "0b001", "0b010", "0b011", "0b100", "0b101", "0b110", "0b111"]
    return valid_binaries_1 + valid_binaries_2 + valid_binaries_3


def generic_generate(prefix: str, good_chars: str, generate_num: int = 10):
    """Generates a valid number."""
    len1 = [f'{prefix}{char}' for char in good_chars]
    return len1 + [f"{prefix}{''.join(sample(good_chars, n))}" for n in range(2, 4) for _ in range(generate_num)]


def generate_valid_hex(generate_num: int = 10):
    """Generates a valid hex number."""
    good_chars = "0123456789ABCDEF"
    prefix = "0x"
    return generic_generate(prefix=prefix, good_chars=good_chars, generate_num=generate_num)


def generate_valid_oct(generate_num: int = 10):
    """Generates a valid octal number."""
    good_chars = "01234567"
    prefix = "0"
    return generic_generate(prefix=prefix, good_chars=good_chars, generate_num=generate_num)


def generate_valid_dec(generate_num: int = 10):
    """Generates a valid binary number."""
    good_chars = "0123456789"
    prefix = ""
    len1 = [f'{char}' for char in good_chars[1:]]
    len2 = [f"{randint(1, 9)}{''.join(sample(good_chars, 1))}" for _ in range(generate_num)]
    len3 = [f"{randint(1, 9)}{''.join(sample(good_chars, 2))}" for _ in range(generate_num)]
    return len1 + len2 + len3


def generic_generate_invalid(good_chars: str, generate_num: int = 10, prefix: str = None):
    """Generates an invalid number of a given base."""
    invalid = list(set(printable[:95]) - set(good_chars) - {"\"", "'", "%", "\\", ";", ":", ","})
    valid = list(set(good_chars))
    prefix = '' if prefix is None else prefix
    # Len 1
    len1 = [f"{prefix}{bad}" for bad in invalid]

    for _ in range(generate_num):
        # Len 2
        # Choose 1 invalid 1 valid
        len2_invalid_1 = ''.join(sample(invalid, 1))
        len2_valid_1 = ''.join(sample(valid, 1))
        len2_1_total = [f"{prefix}{len2_invalid_1}{len2_valid_1}",
                        f"{prefix}{len2_valid_1}{len2_invalid_1}"]

        # Choose 2 invalid
        len2_invalid_2 = sample(invalid, 2)
        len2_2_total = [f"{prefix}{len2_invalid_2[0]}{len2_invalid_2[1]}",
                        f"{prefix}{len2_invalid_2[1]}{len2_invalid_2[0]}"]

        # Len 3
        # Choose 1 invalid 2 valids
        len3_invalid_1 = sample(invalid, 1)
        len3_valid_2 = sample(valid, 2)
        perms_1 = permutations(len3_invalid_1 + len3_valid_2, 3)
        len3_1_total = [f"{prefix}{''.join(p)}" for p in perms_1]

        # Choose 2 invalid 1 valid
        len3_invalid_2 = sample(invalid, 2)
        len3_valid_1 = sample(valid, 1)
        perms_2 = permutations(len3_invalid_2 + len3_valid_1, 3)
        len3_2_total = [f"{prefix}{''.join(p)}" for p in perms_2]

        # Choose 3 invalids
        len3_invalid_3 = sample(invalid, 3)
        perms_3 = permutations(len3_invalid_3, 3)
        len3_3_total = [f"{prefix}{''.join(p)}" for p in perms_3]
        final_lis = len1 + len2_1_total + len2_2_total + len3_1_total + len3_2_total + len3_3_total
        
        # For octal, don't use bad inputs where the second character is another prefix
        if prefix == "0":
            final_lis = [s for s in final_lis if (len(s) > 1 and s[1] not in ['x', 'b'])]

        return final_lis