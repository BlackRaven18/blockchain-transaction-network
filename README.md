# Blockchain Transaction Network
The application implements a blockchain network that enables the transfer of documents between network users. Communication between nodes in the blockchain network is conducted using the WebSocket protocol. The nodes ensure the consistency of the network and collaborate during the voting process to validate transactions and mine new blocks within the network.

Application employs an implemented Proof of Work consensus algorithm to ensure data consistency and integrity within the network.

Application uses a Redis database to store the state of the blockchain on each node.

Blockchain network features a graphical user interface that allows users to monitor the current state of the network and individual nodes, as well as view ongoing operations performed by the nodes in real time.

Clients using the network sign each transaction with a digital signature, which is later verified by the nodes in the network. In the case of a mismatch, transactions are deemed fraudulent and are rejected.

Additionally, the application allows for injecting node faults into the network to analyze its behavior in the event of issues. Fault injection includes:
- Node malfunction
- Rejecting every transaction by a node
- Not participating in the process of mining a new block

## Screenshots
| Main page | Launched network | Registering client |
| -------|--------------|-----------------|
| <img src="https://github.com/user-attachments/assets/273f7775-6e16-4a0d-90ff-83b55cb3f75f" width="400"> | <img src="https://github.com/user-attachments/assets/dc7766f2-88f6-4798-8e86-ba2f77d27b6a" width="400"> | <img src="https://github.com/user-attachments/assets/fdad6b24-729b-4736-ae46-d6790b32d31c" width="400">|

| Node details | Registered clients | Blockchain state |
| -------|--------------|-----------------|
| <img src="https://github.com/user-attachments/assets/c01e551c-5a53-4592-8822-2bc25e769758" width="400"> | <img src="https://github.com/user-attachments/assets/b484352b-1fd0-4773-81a7-9200c6973181" width="400"> | <img src="https://github.com/user-attachments/assets/b41a32ec-bca3-44a4-a417-dca9310ec6f6" width="400"> |

| Health check | Voting over transaction | Mining |
| -------|--------------|-----------------|
| <img src="https://github.com/user-attachments/assets/e33e7161-c7d9-47fb-b780-e8b478266377" width="400"> | <img src="https://github.com/user-attachments/assets/a82cd7b1-9fd7-42fe-aef3-430312ff9a52" width="400"> | <img src="https://github.com/user-attachments/assets/1344751f-dbf6-4aad-915d-b8d1647389c2" width="400">

## Technologies Used:

- **Python:** A powerful programming language used for the backend development and blockchain functionality.
- **TypeScript:** A typed superset of JavaScript used for building robust frontend applications with React.
- **Redis:** A fast, in-memory data store used for storing the blockchain state on each node.
- **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python, used for backend development.
- **React:** A JavaScript library for building user interfaces, used for the frontend of the application.

## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
    - [Network](#network)
    - [Frontend](#frontend)
- [Functionalities](#functionalities)

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites
- Python >=3.12
- Pip: 24.0
- Node.js: 20.11.1
- npm: 10.9.2
- Docker: >= 27.2.0
- Docker Compose: >= 1.29

> Note: Redis is a required component of the application, but it is automatically managed and launched via Docker Compose. No manual installation of Redis is needed.

### Installing
Clone the repository:
```bash
git clone https://github.com/BlackRaven18/blockchain-transaction-network.git
```

#### Network

1. Navigate to the network folder:
    ```bash
    cd network
    ```
   
2. (Optional) Create a virtual environment (recommended):
    ```bash
    # Windows
    python -m venv venv

    # Linux/macOS
    python3 -m venv venv
    ```

    Activate the virtual environment
    ```bash
    # Windows
    venv\Scripts\activate
    
    # Linux/macOS
    source venv/bin/activate
    ```

3. Install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the launcher: <br />
   Navigate to directory with launcher:
   ```bash
   cd launcher
   ```
    
   Run launcher with FastAPI CLI
   ```bash
   fastapi dev main.py
   ```
   
5. Run the client:<br />
    Navigate to directory with network client:
   ```bash
   cd client
   ```

    Run client with uvicorn
   ```bash
   python .\main.py --port 8010 --id client1
   ```
   
#### Frontend
1. Navigate to the frontend folder:
    ```bash
    cd frontend
    ```

2. Install the required dependencies:
    ```bash
    npm install
    ```

3. Run the React application:
    ```bash
    npm start
    ```

### Functionalities:

- **Document Transmission:**
  - **Document Exchange:** Enable secure transmission of documents between clients in the network.

- **Transaction Validation:**
  - **Node Voting:** Nodes collaboratively vote to validate transactions within the blockchain network.

- **Blockchain Operations:**
  - **Block Mining:** Perform the mining of new blocks to add them to the blockchain.
  - **Block Verification:** Verify the correctness and integrity of blocks before they are added to the chain.

- **Network Monitoring:**
  - **Real-Time Network Overview:** View the network’s operations, including ongoing transactions and node activities, in real time.

- **Fault Injection:**
  - **Simulated Errors:** Inject node faults to analyze network behavior under problematic conditions.

- **Node Monitoring:**
  - **Node State Overview:** Inspect the current state and performance of individual nodes within the network.
