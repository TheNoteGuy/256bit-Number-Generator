import random
from decimal import Decimal, getcontext

getcontext().prec = 1000


def generate_bool_array(sign=None, exponent_value=None, random_mantissa=True):
    bool_array = [False] * 256

    if sign is not None:
        bool_array[0] = sign < 0
    else:
        bool_array[0] = random.choice([True, False])

    if exponent_value is not None:
        bias = 2 ** 18 - 1
        biased_exp = exponent_value + bias
        for i in range(19):
            bool_array[i + 1] = bool((biased_exp >> (18 - i)) & 1)
    else:
        for i in range(1, 20):
            bool_array[i] = random.choice([True, False])

    if random_mantissa:
        for i in range(20, 256):
            bool_array[i] = random.choice([True, False])

    return bool_array


def convert_to_float256(bool_array):
    sign = -1 if bool_array[0] else 1
    exponent = sum(2 ** (18 - i) for i in range(19) if bool_array[i + 1])
    adjusted_exponent = exponent - (2 ** 18 - 1)
    mantissa = sum(Decimal(2) ** Decimal(-(i + 1)) for i in range(236) if bool_array[i + 20])
    final_value = Decimal(sign) * Decimal(2) ** Decimal(adjusted_exponent) * (Decimal(1) + mantissa)
    return final_value


def print_float256_details(bool_array):
    print("\nCOMPONENT ANALYSIS:")
    print(f"Sign bit: {'Negative (1)' if bool_array[0] else 'Positive (0)'}")
    exponent_bits = ''.join('1' if b else '0' for b in bool_array[1:20])
    print(f"Exponent bits: {exponent_bits}")
    mantissa_bits = ''.join('1' if b else '0' for b in bool_array[20:256])
    print(f"Mantissa bits: {mantissa_bits}")

    result = convert_to_float256(bool_array)
    print(f"\nFINAL VALUE: {result}")

    if abs(result) == 0:
        print("This is zero!")
    elif abs(result) == float('inf'):
        print("This is infinity!")
    elif abs(result) > 10 ** 100:
        print("This is a very large number!")
    elif abs(result) < 10 ** -100:
        print("This is a very small number!")
    else:
        print("This is a normal-sized number!")


if __name__ == "__main__":
    print("Generating random 256-bit float...")
    bool_array = generate_bool_array()
    print_float256_details(bool_array)