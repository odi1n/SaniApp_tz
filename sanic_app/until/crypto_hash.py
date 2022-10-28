from Crypto.Hash import SHA256, SHA1


def decrypto(private_key, transaction_id, user_id, bill_id, amount):
    signature = SHA1.new(f'{private_key}:{transaction_id}:{user_id}:{bill_id}:{amount}'.encode()).hexdigest()
    return signature
