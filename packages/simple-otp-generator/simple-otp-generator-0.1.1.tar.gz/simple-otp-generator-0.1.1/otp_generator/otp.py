# otp_generator/otp.py

import random
import string

def generate_otp(length=6, include_digits=True, include_uppercase=True, include_lowercase=True):
    """
    Generates a One Time Password (OTP) with the specified characteristics.

    Parameters:
    - length (int): The length of the OTP. Must be a positive integer.
    - include_digits (bool): If True, include digits in the OTP.
    - include_uppercase (bool): If True, include uppercase letters in the OTP.
    - include_lowercase (bool): If True, include lowercase letters in the OTP.

    Returns:
    - str: The generated OTP.

    Raises:
    - ValueError: If the length is not a positive integer or if no character type is selected.
    """
    try:
        if not isinstance(length, int) or length <= 0:
            raise ValueError("Length must be a positive integer")

        characters = ''
        if include_digits:
            characters += string.digits
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_lowercase:
            characters += string.ascii_lowercase

        if not characters:
            raise ValueError("At least one character type must be included")

        otp = ''.join(random.choice(characters) for _ in range(length))
        return otp

    except ValueError as e:
        return str(e)

    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
