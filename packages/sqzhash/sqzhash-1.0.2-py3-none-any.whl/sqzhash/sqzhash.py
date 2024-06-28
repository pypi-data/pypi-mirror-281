import random

class SqzHash:
    def __init__(self):
        self.prime1 = 0xA5A5A5A5A5A5A5A5
        self.prime2 = 0x5A5A5A5A5A5A5A5A
        self.prime3 = 0x3C3C3C3C3C3C3C3C
        self.prime4 = 0xC3C3C3C3C3C3C3C3
        self._reset()

    def _reset(self):
        self.hash_value1 = self.prime1
        self.hash_value2 = self.prime2
        self.hash_value3 = self.prime3
        self.hash_value4 = self.prime4

    def update(self, input_data):
        if isinstance(input_data, str):
            input_data = input_data.encode('utf-8')
        for byte in input_data:
            self.hash_value1 = (self.hash_value1 * self.prime1 + byte) % 2 ** 64
            self.hash_value2 = (self.hash_value2 * self.prime2 + byte) % 2 ** 64
            self.hash_value3 = (self.hash_value3 * self.prime3 + byte) % 2 ** 64
            self.hash_value4 = (self.hash_value4 * self.prime4 + byte) % 2 ** 64
            self._mix_hash_values()

    def _mix_hash_values(self):
        self.hash_value1 ^= (self.hash_value2 >> 16) | (self.hash_value3 << 16)
        self.hash_value2 ^= (self.hash_value3 >> 16) | (self.hash_value4 << 16)
        self.hash_value3 ^= (self.hash_value4 >> 16) | (self.hash_value1 << 16)
        self.hash_value4 ^= (self.hash_value1 >> 16) | (self.hash_value2 << 16)

    def _finalize(self):
        self.hash_value1 ^= (self.hash_value2 << 16) | (self.hash_value3 >> 16)
        self.hash_value2 ^= (self.hash_value3 << 16) | (self.hash_value4 >> 16)
        self.hash_value3 ^= (self.hash_value4 << 16) | (self.hash_value1 >> 16)
        self.hash_value4 ^= (self.hash_value1 << 16) | (self.hash_value2 >> 16)

    def _destroy(self):
        self.hash_value1 = random.getrandbits(64)
        self.hash_value2 = random.getrandbits(64)
        self.hash_value3 = random.getrandbits(64)
        self.hash_value4 = random.getrandbits(64)
        self.prime1 = random.getrandbits(64)
        self.prime2 = random.getrandbits(64)
        self.prime3 = random.getrandbits(64)
        self.prime4 = random.getrandbits(64)

    def hexdigest(self):
        self._finalize()
        combined_hash = (self.hash_value1 << 192) | (self.hash_value2 << 128) | (
                self.hash_value3 << 64) | self.hash_value4
        hex_hash = format(combined_hash, '064x')
        self._destroy()
        return hex_hash


def hash_string(input_string):
    hasher = SqzHash()
    hasher.update(input_string)
    return hasher.hexdigest()


def hash_file(file_path):
    hasher = SqzHash()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()