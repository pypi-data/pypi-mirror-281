from setuptools import setup, find_packages

setup(
    name='sqzhash',
    version='1.0.0',
    description='SqzHash is a custom cryptographic hash algorithm implementation designed to compute hash values for strings and files. The algorithm combines shifts, XOR operations, and the use of prime numbers to efficiently and reliably compute unique hash sums for various data types.',
    author='Squizoff',
    packages=find_packages(),
    python_requires='>=3.6',
)