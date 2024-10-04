import config
import weaviate
import weaviate.classes.config as wc
import weaviate.classes as wvc
import argparse
import sys

parser = argparse.ArgumentParser(description="Create a schema in Weaviate")
parser.add_argument("--delete", action="store_true", help="Delete the collection if it already exists")
args = parser.parse_args()

client = config.weaviate_client()
print("connected to Weaviate...")

collection_name = config.COLLECTION_NAME

if client.collections.exists(collection_name):
    
    if args.delete:
        client.collections.delete(collection_name)
        print("Collection already exists. Deleted.")
    else:
        print("Collection already exists. Nothing to do.")
        client.close()
        sys.exit(0)

try:
    client.collections.create(
        name=collection_name,
        properties=[
            wc.Property(name="title", data_type=wc.DataType.TEXT),
            wc.Property(name="content", data_type=wc.DataType.TEXT),
            wc.Property(name="chunk", data_type=wc.DataType.TEXT),
        ],
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
        generative_config=wvc.config.Configure.Generative.openai(),
    )
except Exception as e:
    print(f"An error occurred: {e}")
else:
    print("Schema created")

client.close()
print("closing session...")