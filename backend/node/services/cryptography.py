from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from schemas.transaction import Transaction
from repositories.public_key import get_public_key

def verify_transaction(transaction: Transaction) -> str:

    if not transaction.signature:
        print("No signature to verify")
        return "invalid"  # No signature to verify
    
    sender_public_key_pem = get_public_key(transaction.sender)

    if sender_public_key_pem is None:
        print("Public key not found")
        return "invalid"
    
    receiver = get_public_key(transaction.recipient)

    if receiver is None:
        print("Receiver do not exist")
        return "invalid"
    
    sender_public_key = serialization.load_pem_public_key(sender_public_key_pem.encode('utf-8'))

    serialized_data = transaction.serialize()
    try:
        sender_public_key.verify(
            bytes.fromhex(transaction.signature),
            serialized_data.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return "valid"
    except Exception:
        return "invalid" 