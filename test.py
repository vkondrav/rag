import config
import weaviate
from weaviate.classes.query import MetadataQuery
import json
import tiktoken

client = config.weaviate_client()

collection = client.collections.get(config.COLLECTION_NAME)
response = collection.query.near_text(
    query="onboarding",
    limit=2,
    return_metadata = MetadataQuery(distance=True)
)

client.close()

mapped_objects = [{'title': o.properties['title'], 'content': o.properties['content']} for o in response.objects]
json_output = json.dumps(mapped_objects, indent = 4)
print(json_output)