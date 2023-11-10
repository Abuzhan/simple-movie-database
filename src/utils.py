import random
import string


def generate_random_string():
    return ''.join(
        random.choices(
            string.ascii_uppercase + string.digits + string.ascii_lowercase, k=16
        )
    )


__all__ = [
    'generate_random_string',
]
