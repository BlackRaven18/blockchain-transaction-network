
from cryptography.hazmat.primitives import serialization

def get_public_key():
    with open("src/keys/public.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
            )

    return public_key