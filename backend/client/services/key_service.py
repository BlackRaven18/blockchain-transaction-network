from cryptography.hazmat.primitives import serialization

def get_private_key():
    with open("keys/private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            )

    return private_key