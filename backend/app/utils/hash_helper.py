"""
hash_helper.py — Cryptographic hash generator and verification utility.

Provides simple SHA-256 and BLAKE2b hashing for strings and bytes.
"""

import hashlib
from typing import Literal


def hash_string(text: str, algorithm: Literal["sha256", "blake2b"] = "sha256") -> str:
    """
    Compute the hex digest of a string using the specified algorithm.

    Args:
        text: The input string to hash.
        algorithm: 'sha256' (default) or 'blake2b'.

    Returns:
        Hex-encoded digest string.
    """
    encoded = text.encode("utf-8")
    if algorithm == "blake2b":
        return hashlib.blake2b(encoded).hexdigest()
    return hashlib.sha256(encoded).hexdigest()


def verify_hash(text: str, expected_hash: str, algorithm: Literal["sha256", "blake2b"] = "sha256") -> bool:
    """
    Verify whether a string matches a known hex digest.

    Args:
        text: The original string to verify.
        expected_hash: The expected hex digest.
        algorithm: Hashing algorithm used to produce the expected_hash.

    Returns:
        True if the hash matches, False otherwise.
    """
    return hash_string(text, algorithm) == expected_hash


def hash_bytes(data: bytes, algorithm: Literal["sha256", "blake2b"] = "sha256") -> str:
    """
    Compute the hex digest of raw bytes.

    Args:
        data: The raw bytes to hash.
        algorithm: 'sha256' (default) or 'blake2b'.

    Returns:
        Hex-encoded digest string.
    """
    if algorithm == "blake2b":
        return hashlib.blake2b(data).hexdigest()
    return hashlib.sha256(data).hexdigest()
