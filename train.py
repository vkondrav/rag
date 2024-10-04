import config
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

import weaviate.classes as wvc
import weaviate

import tiktoken

def split_txt_content(txt_path):

    try:
        loader = TextLoader(txt_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 50,
            length_function = len,
            is_separator_regex = False,
        )

        return text_splitter.split_documents(documents)
    except Exception as e:
        print(f"Skipping chunking of file {txt_path} due to error: {e}")
        return []

def upload_to_weaviate(filename: str, chunks, collection):

    try:
        
        if chunks is None or len(chunks) == 0:
            throw("No chunks to upload")

        with collection.batch.dynamic() as batch:
            for i, chunk in enumerate(chunks):
                chunk_id = f"{filename}-chunk-{i}"
                data_row = {
                    "title": filename,
                    "content": chunk.page_content,
                    "chunk": chunk_id
                }
                batch.add_object(properties = data_row)
                print(f"Queued chunk {chunk_id} of document {filename} for upload.")

        if collection.batch.failed_objects:
            print("Some objects failed to upload:")
            print(collection.batch.failed_objects[0])
        else:
            response = collection.aggregate.over_all(total_count=True)
            print(f"Finished uploading document {filename} to Weaviate with a total of {response.total_count} chunks.")
    except Exception as e:
        print(f"Skipping file {filename} due to error: {e}")

def process_files_in_directory(directory_path, weaviate_client):

    for filename in os.listdir(directory_path):
        
        if filename.startswith('.'):
            continue

        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            chunks = split_txt_content(file_path)
            upload_to_weaviate(filename, chunks, weaviate_client)
        else:
            process_files_in_directory(file_path, weaviate_client)

client = config.weaviate_client()

collection_name = config.COLLECTION_NAME

collection_exists = client.collections.exists(collection_name)

if collection_exists:
    collection = client.collections.get(collection_name)
    collection_total_count = collection.aggregate.over_all(total_count=True).total_count
    if collection_total_count > 0:
        print("Collection already exists and populated. No training needed.")
    else:
        process_files_in_directory('data', collection)
else:
    print("Collection does not exist. Please run schema.py first.")

client.close()