import hashlib as HL
import os

def generate_salt():
    randoms = "".join([str(os.urandom(8192), "utf-8") for _ in range(100)])
    return HL.sha512(randoms).hexdigest()

def hash_password(password: str, salt: str):
    return HL.pbkdf2_hmac("sha512", bytes(password, "utf-8"), bytes(salt, "utf-8"), 500000).hex()

def check_password(saved_password_hash: str, saved_salt: str, inputted_plain_password: str):
    hashed_plain = hash_password(inputted_plain_password, saved_salt)
    return hashed_plain == saved_password_hash