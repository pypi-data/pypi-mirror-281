# SqzHash

SqzHash is a custom cryptographic hash algorithm implementation designed to compute hash values for strings and files. The algorithm combines shifts, XOR operations, and the use of prime numbers to efficiently and reliably compute unique hash sums for various data types.

## Installation

You can install SqzHash using pip:

```sh
pip install sqzhash
```

# Example Usage
## Hashing a String
You can use the hash_string function to compute the hash of a string.
```python
from sqzhash import hash_string

input_string = "example string"
hash_value = hash_string(input_string)
print(f"Hash value for the string is: {hash_value}")
```

## Hashing a File
You can use the hash_file function to compute the hash of a file.
```python
from sqzhash import hash_file

file_path = "path/to/your/file.txt"
hash_value = hash_file(file_path)
print(f"Hash value for the file is: {hash_value}")
```