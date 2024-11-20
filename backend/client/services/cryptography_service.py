from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from schemas.transaction import Transaction
from services.key_service import generate_keys

private_key, public_key = generate_keys()

def sign_transaction(transaction: Transaction) -> str:

    serialized_data = transaction.serialize()
    signature = private_key.sign(
        serialized_data.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature.hex() 