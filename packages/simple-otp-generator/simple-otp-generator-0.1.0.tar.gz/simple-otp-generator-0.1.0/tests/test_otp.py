# tests/test_otp.py

import unittest
from otp_generator.otp import generate_otp

class TestGenerateOtp(unittest.TestCase):

    def test_length(self):
        self.assertEqual(len(generate_otp(6)), 6)
        self.assertEqual(len(generate_otp(8)), 8)

    def test_include_digits(self):
        otp = generate_otp(10, include_digits=True, include_uppercase=False, include_lowercase=False)
        self.assertTrue(all(c in '0123456789' for c in otp))

    def test_include_uppercase(self):
        otp = generate_otp(10, include_digits=False, include_uppercase=True, include_lowercase=False)
        self.assertTrue(all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' for c in otp))

    def test_include_lowercase(self):
        otp = generate_otp(10, include_digits=False, include_uppercase=False, include_lowercase=True)
        self.assertTrue(all(c in 'abcdefghijklmnopqrstuvwxyz' for c in otp))

    def test_no_characters(self):
        with self.assertRaises(ValueError):
            generate_otp(10, include_digits=False, include_uppercase=False, include_lowercase=False)

if __name__ == "__main__":
    unittest.main()
