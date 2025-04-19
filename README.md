# mini-blockchain-simulator

# 🧱 Mini Blockchain Simulator

A beginner-friendly blockchain simulator built with Python.  
This project demonstrates the fundamental concepts of a blockchain system including wallet creation, transaction signing, block generation, and persistent storage.

---

## 🚀 Features

- 🔐 ECDSA-based wallet system
- 📦 Block structure with SHA-256 hash linking
- 🧾 Transaction creation and pooling
- ⛏ Automatic block generation every 10 seconds
- 💾 JSON-based blockchain file storage
- ✅ Digital signature verification

---

## 📸 Example Output
[Transaction] Alice → Bob: $50 [Transaction] Bob → Charlie: $30 [Block] New block created with 2 transactions (index: 1) Blockchain saved to file: blockchain.json


---

## 🛠 Tech Stack

- Python 3.x
- [`hashlib`](https://docs.python.org/3/library/hashlib.html) – hashing algorithm
- [`ecdsa`](https://pypi.org/project/ecdsa/) – wallet generation & digital signatures
- `threading` – simulate real-time block creation
- `json` – data persistence

---

## 🧑‍💻 Installation & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/mini-blockchain-simulator.git
cd mini-blockchain-simulator

**Install Dependencies**
pip install ecdsa

**Run the Project**
python mini-blockchain-simulator.py




