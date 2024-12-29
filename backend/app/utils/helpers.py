import base64

def encode_binary_data(data):
    if isinstance(data, bytes):
        return base64.b64encode(data).decode('utf-8')  # Convert binary to Base64 string
    return data

from bson import ObjectId

def serialize_mongo_data(data):
    if isinstance(data, list):
        return [{**item, "_id": str(item["_id"])} for item in data]
    elif isinstance(data, dict):
        return {**data, "_id": str(data["_id"])}
    return data
