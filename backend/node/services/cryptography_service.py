from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from schemas.transaction import Transaction
from repositories.keys_repository import get_public_key

def verify_transaction(transaction: Transaction) -> bool:

    if not transaction.signature:
        print("No signature to verify")
        return False  # No signature to verify
    
    public_key_pem = get_public_key(transaction.sender)

    if public_key_pem is None:
        print("Public key not found")
        return False
    
    public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'))

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
