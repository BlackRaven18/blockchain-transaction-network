from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from schemas.transaction import Transaction
from services.key_service import get_private_key

def sign_transaction(transaction: Transaction) -> str:
    private_key = get_private_key()
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