import random
from decimal import Decimal, getcontext

getcontext().prec = 20000  # Increased precision for our massive number


def generate_megafloat(sign=None, exponent_value=None, random_mantissa=True):
    bool_array = [False] * 65536

    if sign is not None:
        bool_array[0] = sign < 0
    else:
        bool_array[0] = random.choice([True, False])

    if exponent_value is not None:
        bias = 2 ** 15 - 1
        biased_exp = exponent_value + bias
        for i in range(16):
            bool_array[i + 1] = bool((biased_exp >> (15 - i)) & 1)
    else:
        for i in range(1, 17):
            bool_array[i] = random.choice([True, False])

    if random_mantissa:
        for i in range(17, 65536):
            bool_array[i] = random.choice([True, False])

    return bool_array


def convert_megafloat(bool_array):
    sign = -1 if bool_array[0] else 1

    exponent = sum(2 ** (15 - i) for i in range(16) if bool_array[i + 1])
    adjusted_exponent = exponent - (2 ** 15 - 1)

    mantissa = sum(Decimal(2) ** Decimal(-(i + 1))
                   for i in range(65519) if bool_array[i + 17])

    final_value = Decimal(sign) * Decimal(2) ** Decimal(adjusted_exponent) * (Decimal(1) + mantissa)
    return final_value


def print_megafloat_details(bool_array):
    print("\nMEGA-FLOAT ANALYSIS:")
    print(f"Sign bit: {'Negative (1)' if bool_array[0] else 'Positive (0)'}")

    exponent_bits = ''.join('1' if b else '0' for b in bool_array[1:17])
    print(f"Exponent bits ({len(exponent_bits)} bits): {exponent_bits}")

    mantissa_bits = ''.join('1' if b else '0' for b in bool_array[17:65536])
    print(f"Mantissa bits ({len(mantissa_bits)} bits): {mantissa_bits[:100]}... [truncated]")
    print(f"Mantissa 1's density: {mantissa_bits.count('1') / len(mantissa_bits):.2%}")

    result = convert_megafloat(bool_array)
    print(f"\nFINAL VALUE: {result}")

    if abs(result) == 0:
        print("This is zero!")
    elif abs(result) == float('inf'):
        print("This is infinity!")
    elif abs(result) > Decimal('10') ** Decimal('1000'):
        print("This is an astronomically large number!")
    elif abs(result) < Decimal('10') ** Decimal('-1000'):
        print("This is an astronomically small number!")
    else:
        print("This is a surprisingly normal number!")


def generate_special_megafloat(type="random"):
    if type == "small":
        return generate_megafloat(sign=1, exponent_value=-1000)
    elif type == "large":
        return generate_megafloat(sign=1, exponent_value=1000)
    elif type == "negative_tiny":
        return generate_megafloat(sign=-1, exponent_value=-2000)
    elif type == "positive_huge":
        return generate_megafloat(sign=1, exponent_value=2000)
    else:
        return generate_megafloat()


if __name__ == "__main__":
    print("Generating random 65536-bit float...")
    bool_array = generate_megafloat()
    print_megafloat_details(bool_array)

    print("\nGenerating a huge number...")
    huge_array = generate_special_megafloat("positive_huge")
    print_megafloat_details(huge_array)