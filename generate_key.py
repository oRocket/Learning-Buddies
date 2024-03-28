#!/usr/bin/python3

import secrets
import string

# Generate a random secret key
def generate_secret_key(length=24):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

# Generate the secret key
secret_key = generate_secret_key()

# Save the secret key to a file named "key"
with open("key", "w") as file:
    file.write(secret_key)

# Print the generated secret key (optional)
print("Secret key:", secret_key)
