# setup.py

from setuptools import setup, find_packages

setup(
    name="simple-otp-generator",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[],
    author="Gaurav Borade",
    author_email="gauravwinjitwork@gmail.com",
    description="A simple OTP generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/otp-generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
