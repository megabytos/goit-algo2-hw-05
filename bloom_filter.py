import mmh3


class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True


def check_password_uniqueness(bloom_filter: BloomFilter, passwords_list: list) -> set:
    if not isinstance(passwords_list, list) or len(passwords_list) == 0:
        raise TypeError(f"Illegal argument for check_password_uniqueness: passwords_list = {passwords_list} must be a non-empty list")
    for pwd in passwords_list:
        if pwd is None or not isinstance(pwd, str) or len(pwd) == 0:
            check_result = "invalid"
        elif bloom_filter.contains(pwd):
            check_result = "already used"
        else:
            check_result = "unique"
            bloom_filter.add(pwd)
        yield pwd, check_result


if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "newpassword", '', True, []]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in results:
        print(f"Password '{password}' - {status}.")
