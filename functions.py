import random
import string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_hash_from_password(password: str):
    return password + "notreallyhashed"

def compare_password_with_hash(password: str, hashed_password: str) -> bool:
    return create_hash_from_password(password) == hashed_password