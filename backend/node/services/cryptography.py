from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from schemas.transaction import Transaction

from repositories.client import get_client

def verify_transaction(transaction: Transaction) -> str:

    if not transaction.signature:
        print("No signature to verify")
        return "invalid"  # No signature to verify
    
    sender = get_client(transaction.sender)

    if sender is None:
        print("Sender not registered as network client")
        return "invalid"
    
    receiver = get_client(transaction.recipient)

    if receiver is None:
        print("Receiver not registered as network client")
        return "invalid"
    
    sender_public_key = serialization.load_pem_public_key(sender.key.encode('utf-8'))

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