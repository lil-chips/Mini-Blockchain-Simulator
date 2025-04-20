import hashlib
import json
import time
import threading
import random
from ecdsa import SigningKey, VerifyingKey, NIST384p
from datetime import datetime  # Import datetime module for formatted date

# -------- Block Structure --------
class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

# -------- Wallet Functions --------
def generate_wallet():
    sk = SigningKey.generate(curve=NIST384p)
    vk = sk.verifying_key
    return sk, vk

def sign_transaction(transaction, sk):
    message = json.dumps(transaction, sort_keys=True).encode()
    return sk.sign(message).hex()

def verify_transaction(transaction, signature, vk):
    message = json.dumps(transaction, sort_keys=True).encode()
    try:
        return vk.verify(bytes.fromhex(signature), message)
    except:
        return False

# -------- Blockchain Initialization --------
def create_genesis_block():
    # Use datetime to get formatted timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d")
    return Block(0, timestamp, "Genesis Block", "0")

def create_new_block(previous_block, transactions):
    # Use datetime to get formatted timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d")
    index = previous_block.index + 1
    return Block(index, timestamp, transactions, previous_block.hash)

def save_blockchain_to_file(blockchain, filename="blockchain.json"):
    with open(filename, 'w') as file:
        json.dump([block.__dict__ for block in blockchain], file, indent=4)

# -------- Transaction Generation --------
def create_transaction(sender_vk_hex, receiver_vk_hex, amount, sender_sk):
    tx = {
        "sender": sender_vk_hex,
        "receiver": receiver_vk_hex,
        "amount": amount
    }
    signature = sign_transaction(tx, sender_sk)
    tx["signature"] = signature
    return tx

# -------- Automatic Block Production --------
def block_producer():
    global blockchain, mempool

    while True:
        if len(mempool) >= 1:
            selected_txs = mempool[:3]  # Maximum of 3 transactions per block
            block = create_new_block(blockchain[-1], selected_txs)
            blockchain.append(block)
            save_blockchain_to_file(blockchain)
            print(f"✅ New block produced! Block number: {block.index}, containing {len(selected_txs)} transactions\n")
            del mempool[:3]
        time.sleep(10)  # Check the mempool every 10 seconds

# -------- Random Transaction Generation --------
def random_transaction_generator():
    while True:
        sender_sk, sender_vk = generate_wallet()
        _, receiver_vk = generate_wallet()

        sender_hex = sender_vk.to_string().hex()
        receiver_hex = receiver_vk.to_string().hex()

        amount = random.randint(1, 100)
        tx = create_transaction(sender_hex, receiver_hex, amount, sender_sk)
        mempool.append(tx)
        print(f"➕ Simulated transaction added: {sender_hex[:6]} → {receiver_hex[:6]} ${amount}")
        time.sleep(random.randint(3, 6))  # Add a new transaction every 3-6 seconds

# -------- Main Program --------
if __name__ == "__main__":
    blockchain = [create_genesis_block()]
    mempool = []

    # Start background threads: block producer and transaction generator
    threading.Thread(target=block_producer, daemon=True).start()
    threading.Thread(target=random_transaction_generator, daemon=True).start()

    # Run forever (can be manually stopped)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program ended, blockchain saved.")
