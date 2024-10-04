import config
from flask import Flask, request, jsonify
import weaviate
from weaviate.classes.query import MetadataQuery
import json

client = config.weaviate_client()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health():
    return jsonify({"client_ready": client.is_ready()})

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data['query']
    print("Received data:", query)
    try:
        print("Querying Weaviate directly...")

        collection = client.collections.get(config.COLLECTION_NAME)

        response = collection.query.near_text(
            query = query,
            limit = 30
        )

        mapped_objects = [{'title': o.properties['title'], 'content': o.properties['content']} for o in response.objects]
        results = json.dumps(mapped_objects, indent = 4)

        print("Search results:", results)
        
        return results

    except Exception as e:
        app.logger.error(f'Error in /search: {e}')
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)