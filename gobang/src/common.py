import hashlib
import random
import string


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_random_hash():
    random_string = generate_random_string()
    hashed_value = hashlib.sha256(random_string.encode()).hexdigest()
    return hashed_value
