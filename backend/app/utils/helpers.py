import pickle
import base64

def convert_embedding_to_base64(embedding):

    """
    Converts a list of embeddings to a base64 encoded string.
    """
    binary_data = pickle.dumps(embedding)  # Serialize to binary
    return base64.b64encode(binary_data).decode('utf-8')  # Encode as base64 string



def convert_base64_to_embedding(base64_string):

    """
    Decodes a base64 string back into the original embedding list.
    """
    binary_data = base64.b64decode(base64_string)  # Decode from base64
    return pickle.loads(binary_data)  # Deserialize from binary



# Test
# emedding = [2,3,34, 43.2, -22, 4]

# _e_b = convert_embedding_to_base64(emedding)
# _b_e = convert_base64_to_embedding(_e_b)

# print(_e_b)
# print(_b_e)