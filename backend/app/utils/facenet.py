from fastapi import HTTPException
from PIL import Image
from facenet_pytorch import InceptionResnetV1, MTCNN
import torch
import numpy as np
import io

# FaceNet Model Setup
model = InceptionResnetV1(pretrained="vggface2").eval()

# MTCNN Setup for face detection
mtcnn = MTCNN(keep_all=True)


def detect_faces(image_data: bytes):
    pil_image = Image.open(io.BytesIO(image_data))
    boxes, _ = mtcnn.detect(pil_image)
    if boxes is None or len(boxes) == 0:
        raise HTTPException(status_code=400, detail="No faces detected in the image.")
    return boxes


def process_face_from_image(image_data: bytes) -> list:
    pil_image = Image.open(io.BytesIO(image_data))
    boxes, _ = mtcnn.detect(pil_image)
    if boxes is None or len(boxes) == 0:
        raise HTTPException(status_code=400, detail="No faces detected in the image.")
    
    embeddings_list = []
    for box in boxes:
        try:
            face = pil_image.crop(box).resize((160, 160))  # Crop and resize for FaceNet
            img_array = np.array(face) / 255.0  # Normalize image
            if img_array.shape != (160, 160, 3):
                raise ValueError("Image must be RGB and of size 160x160.")

            # Convert to PyTorch tensor
            img_tensor = torch.tensor(img_array, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0)  # CHW + batch
            embeddings = model(img_tensor).detach().numpy().flatten().tolist()
            embeddings_list.append(embeddings)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing face: {str(e)}")

    return embeddings_list


# with open("passport.min.jpg", "rb") as img_file:
#     image_bytes = img_file.read()

# embeddings = process_face_from_image(image_bytes)
# print(len(embeddings[0]))
