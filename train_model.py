
import cv2
import numpy as np
from PIL import Image
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataset'

def get_images_and_labels(path):
    faces = []
    ids = []

    for image in os.listdir(path):
        img_path = os.path.join(path, image)
        img = Image.open(img_path).convert('L')
        img_np = np.array(img, 'uint8')
        user_id = int(image.split('_')[1])
        faces.append(img_np)
        ids.append(user_id)

    return faces, np.array(ids)

faces, ids = get_images_and_labels(path)
recognizer.train(faces, ids)
recognizer.save('trainer.yml')

