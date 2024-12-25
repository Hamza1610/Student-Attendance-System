import base64

def encode_binary_data(data):
    if isinstance(data, bytes):
        return base64.b64encode(data).decode('utf-8')  # Convert binary to Base64 string
    return data
