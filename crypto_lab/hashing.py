"""SHA-256 and birthday-bound collision experiments on truncated digests."""
import hashlib
import secrets


def sha256_hex(message: bytes) -> str:
    return hashlib.sha256(message).hexdigest()


def find_truncated_collision(digest_bytes: int = 2, max_trials: int = 200_000):
    """Find two different messages with matching *truncated* SHA-256 digests.

    Intended for 1-2 bytes only. This is NOT a collision for full SHA-256.
    """
    if digest_bytes not in (1, 2):
        raise ValueError('Use only 1 or 2 bytes in this bounded educational demo')
    seen = {}
    for attempts in range(1, max_trials + 1):
        sample = secrets.token_bytes(12)
        digest = hashlib.sha256(sample).digest()[:digest_bytes]
        earlier = seen.get(digest)
        if earlier is not None and earlier != sample:
            return earlier, sample, digest.hex(), attempts
        seen[digest] = sample
    raise RuntimeError('Collision not found in bounded trial budget')
