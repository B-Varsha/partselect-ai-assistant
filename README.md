PartSelect AI Assistant
=======================

A fully containerized Retrieval-Augmented Generation (RAG) system designed to help users find refrigerator and dishwasher parts using a hybrid search mechanism and LLM-powered responses.

* * * * *

Features
--------

-   React Frontend with a simple, intuitive chat UI.

-   FastAPI Backend exposing a /chat endpoint for handling user queries.

-   Hybrid Retrieval Pipeline for high-accuracy searches:

    -   Exact part-number matching (e.g., PS123456).

    -   Semantic vector search using MiniLM embeddings.

-   Persistent ChromaDB Vector Store for reliable data storage.

-   DeepSeek LLM for context-based LLM inference.

-   Docker Compose for easy, one-command, fully reproducible deployment.

-   Synthetic CSV Dataset is used to train the system (due to real-world scraping restrictions).

* * * * *

Getting Started
---------------

### 1\. Clone the Repository

```
git clone https://github.com/B-Varsha/partselect-ai-assistant
cd partselect-ai-assistant

```

### 2\. Add Environment Variables

Create a file named .env inside the backend/ directory and add your DeepSeek API key:

```
# backend/.env
DEEPSEEK_API_KEY=your_api_key_here

```

### 3\. Build the Vector Database

Navigate to the backend directory and run the script to process the CSV data and build the persistent ChromaDB store.

```
cd backend
python build_vector_db.py

```

### 4\. Start the System with Docker

From the project root directory, use docker compose to build all images and start the services (Frontend, Backend, ChromaDB).

```
docker compose up --build

```

Access the applications:

| **Service** | **Address** |
| --- | --- |
| Frontend (Chat UI) | http://localhost:3000 |
| Backend (FastAPI) | http://localhost:8001/chat |

* * * * *

Project Structure
-----------------

```
.
├── frontend/                     # React client source code
├── backend/
│   ├── main.py                   # FastAPI server, retrieval logic, and LLM orchestration
│   ├── build_vector_db.py        # Script for embedding data and loading ChromaDB
│   ├── partselect_products.csv   # The synthetic product dataset
│   └── chromadb_store/           # Persistent directory for the vector database
└── docker-compose.yml            # Defines the multi-container application
```
