import cv2
import os
from pathlib import Path

files = os.listdir()

for img in files:
    print(img)
    image = cv2.imread(str(img))
    print(image.shape)
