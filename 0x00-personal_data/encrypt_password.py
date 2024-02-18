#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    The function `hash_password` takes a string password as input,
    encodes it, and then generates a hashed password using bcrypt
    with a randomly generated salt.
    """
    encode = password.encode('utf-8')
    return bcrypt.hashpw(encode, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    The function `is_valid` checks if a given password matches a
    hashed password using the bcrypt algorithm.
    """
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False
