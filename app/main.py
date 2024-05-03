from flask import Flask, request, jsonify
from pymongo import MongoClient,IndexModel, ASCENDING
import os

app = Flask(__name__)

from pymongo.errors import DuplicateKeyError
client = MongoClient(host=os.environ['MONGO_HOST'], port=27017)
db = client.mydatabase
collection = db.mycollection
index = IndexModel([('key', ASCENDING)], unique=True)
collection.create_indexes([index])
@app.route('/', methods=['GET', 'POST', 'PUT'])
def handle_data():
    if request.method == 'GET':
        print('ccccc')
        key = request.args.get('key')
        print('aaaaa')
        if key:
            print('bbbb')
            data = collection.find_one({'key': key})
            if data:
                return jsonify({'value': data['value']})
            else:
                return jsonify({'error': 'Key not found'}), 404
        else:
            all_data = collection.find()
            result = [{'key': item['key'], 'value': item['value']} for item in all_data]
            return jsonify(result)
    elif request.method == 'POST':
        data = request.get_json()
        if 'key' in data and 'value' in data:
            try:
                collection.insert_one(data)
                return jsonify({'message': 'Data created'}), 201
            except DuplicateKeyError:
                return jsonify({'error': 'Key already exists'}), 409
        else:
            return jsonify({'error': 'Missing key or value'}), 400

    elif request.method == 'PUT':
        data = request.get_json()
        if 'key' in data and 'value' in data:
            result = collection.update_one({'key': data['key']}, {'$set': {'value': data['value']}})
            if result.modified_count:
                return jsonify({'message': 'Data updated'})
            else:
                return jsonify({'error': 'Key not found'}), 404
        else:
            return jsonify({'error': 'Missing key or value'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)