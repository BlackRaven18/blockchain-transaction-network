from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from schemas.transaction import Transaction
from services.key_service import get_public_key

def verify_transaction(transaction: Transaction) -> bool:
    if not transaction.signature:
        return False  # No signature to verify
    
    public_key = get_public_key()

    serialized_data = transaction.serialize()
    try:
        public_key.verify(
            bytes.fromhex(transaction.signature),
            serialized_data.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False 
