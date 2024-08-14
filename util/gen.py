"""
Python SECRET_KEY generator.
"""

import random

chars = 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHI\
    JKLMNOPQRSTUVWXYZ!?@#$%^&*()'
size = 50
secret_key = ''.join(random.sample(chars, size))

print(secret_key)
