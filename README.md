# RAG

## Overview
This repository enables a Retrieval-Augmented Generation (RAG) system using Weaviate and OpenAI models.
It is intended for learning purposes. Follow the steps below to set up your development environment, configure your schema, and train the RAG model. You will then connect your model to a custom GPT in ChatGPT (Plus Account Required)

## Prerequisites
- Docker and Docker Compose
- Visual Studio Code (VS Code) with the Remote - Containers extension
- Access to OpenAI API (API key)
- [Ngrok](https://ngrok.com/) (for tunneling, ChatGPT needs a secure https endpoint)

## Setting Up the Development Environment

### Dev Container (Recommended)

This repository includes a development container (`devcontainer`) configuration for a consistent and isolated environment. To run Weaviate you will need to use docker anyway, so best not to set up local. 

1. **Open the Repository in VS Code:**
   - Open the project directory in Visual Studio Code.
   - Ensure you have the Remote - Containers extension installed.

2. **Reopen in the Dev Container:**
   - Click on the green icon in the bottom-left corner of VS Code.
   - Select "Reopen in Container" from the menu.
   - VS Code will now build and start the container as defined in `.devcontainer/devcontainer.json`.

3. **Set Up Environment Variables:**
   - Create a `.env` file in the root directory with the following variables:
     ```env
     OPENAI_APIKEY=<your_openai_api_key>
     WEAVIATE_HOST=localhost
     NGROK_AUTHTOKEN=<your_ngrok_auth_token>
     ```

4. **Set Up Docker:**
   - Start the services using Docker Compose:
     ```bash
     docker-compose up -d
     ```

## Setting Up the Schema

1. **Create the Schema in Weaviate:**
   - Run the schema script:
     ```bash
     python schema.py
     ```
   - The script will create a collection (default: "RAGCollection") in Weaviate with fields for `title`, `content`, and `chunk`. If the collection already exists, it will prompt you to delete or skip this step.

2. **Delete Existing Schema (if needed):**
   - Use the `--delete` flag to delete the existing schema:
     ```bash
     python schema.py --delete
     ```

## Training the RAG Model

1. **Data Preparation:**
   - Place all your training data (text files) in a `data` directory within the root of the repository.

2. **Run the Training Script:**
   - Execute the `train.py` script to process and upload data to Weaviate:
     ```bash
     python train.py
     ```
   - The script splits the text documents into smaller chunks and uploads them to the Weaviate collection. If the collection already contains data, it will skip the training step.

## Running the Application

1. **Start the Application:**
   - Run the main application script:
     ```bash
     python app.py
     ```
   - The app will start a Flask server on port 5001.

2. **Access the Application:**
   - You can interact with the RAG model through the API. Access the health check endpoint:
     ```bash
     curl http://localhost:5001/
     ```

3. **Searching with RAG:**
   - You can perform a search by sending a POST request to the `/search` endpoint with a JSON body containing the query:
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"query": "your_search_query"}' http://localhost:5001/search
     ```

## Scripts Overview

You can interact with the Weaviate container directly from your `.devcontainer` by changing the `WEAVIATE_HOST=localhost`

- **`schema.py`**: Creates a schema in Weaviate to store documents. Allows schema deletion with the `--delete` flag.
- **`train.py`**: Processes and uploads text data into the Weaviate collection.
- **`app.py`**: Runs a Flask server to interact with the RAG model via a REST API.
- **`fetch-books.py` and `fetch-repo.py`**: Utilities for fetching data (e.g., from Project Gutenberg).
- **`config.py`**: Contains configuration settings for connecting to the Weaviate instance.
- **`run.sh`**: Installs dependencies and runs scripts in the proper order (`schema.py`, `train.py`, `app.py`).

## Setting up ChatGPT
TBD

## Closing Notes

- **Error Handling:** All scripts contain basic error handling to provide clear messages if something goes wrong during the schema setup, training, or querying phases.
- **Modifying Schema:** If you need to change the schema (e.g., adding new fields), update the `schema.py` script accordingly and rerun it.

Feel free to contribute or raise issues if you encounter any problems during setup or use!