import os
from os import listdir
path=r'C:\Users\santo\Documents\GitHub\UAS_software\images'
for images in os.listdir(path):
 
    # check if the image ends with png
    if (images.endswith(".png")):
        print(images)