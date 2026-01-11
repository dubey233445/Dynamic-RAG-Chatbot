# Dynamic RAG Chatbot

A Python-based RAG (Retrieval-Augmented Generation) chatbot that dynamically updates its knowledge base by monitoring a local directory for new documents.

## Features

- **Dynamic Ingestion**: Automatically detects new or modified text files in the `data/` directory and adds them to the vector database.
- **Vector Search**: Uses ChromaDB for efficient storage and retrieval of document embeddings.
- **Local Embeddings**: Uses `sentence-transformers` for creating embeddings locally (no API key required for embeddings).
- **Interactive Chat**: Simple CLI interface for querying the knowledge base.

## Prerequisites

- Python 3.9+
- [Optional] An OpenAI API Key if you wish to switch from the dummy LLM to a real one (modify `src/bot.py`).

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the Chatbot**:
    Run the main script to start the file watcher and the chat interface:
    ```bash
    python src/main.py
    ```

2.  **Add Knowledge**:
    - Drop any `.txt` file into the `data/` directory.
    - The system will automatically ingest it.
    - You will see logs in the console indicating "New file detected" and "Successfully ingested".

3.  **Chat**:
    - Ask questions in the terminal.
    - The bot will retrieve relevant chunks from your documents and generate a response.

## internal Architecture

- `src/main.py`: Entry point. Starts the `watchdog` observer and the `Chatbot` loop.
- `src/watcher.py`: Handles file system events (created/modified) and triggers ingestion.
- `src/ingest.py`: Loads text files, splits them into chunks, and stores embeddings in ChromaDB.
- `src/bot.py`: Defines the `Chatbot` class, including the retrieval chain.

## Troubleshooting

- **Import Errors**: Ensure you have installed all requirements.
  ```bash
  pip install chromadb watchdog sentence-transformers langchain langchain-community langchain-huggingface langchain-chroma
  ```
- **Numpy/TensorFlow conflicts**: If you see numpy errors, try installing a compatible version:
  ```bash
  pip install "numpy<2"
  ```
