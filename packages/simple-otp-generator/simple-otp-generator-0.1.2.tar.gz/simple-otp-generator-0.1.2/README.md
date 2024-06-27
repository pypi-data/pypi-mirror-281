
# Simple OTP Generator

A simple and flexible OTP (One Time Password) generator package.

## Features

- Generate OTPs with customizable length
- Include digits, uppercase letters, and lowercase letters
- Error handling for invalid inputs

## Installation

You can install the package using pip:

    pip install simple-otp-generator

## Usage

    from otp_generator.otp import generate_otp 
    
    print(generate_otp(length=6, include_digits=True, include_lowercase=False,include_uppercase=True))enter code here

