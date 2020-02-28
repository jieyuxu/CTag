#!/usr/bin/env python

from google.cloud import vision

# sample label detection
image_uri = 'gs://cloud-samples-data/vision/using_curl/shanghai.jpeg'

client = vision.ImageAnnotatorClient()
image = vision.types.Image()
image.source.image_uri = image_uri

response = client.label_detection(image=image)

print('Labels (and confidence score):')
print('=' * 79)
for label in response.label_annotations:
    print(f'{label.description} ({label.score*100.:.2f}%)')

# Labels (and confidence score):
# ===============================================================================
# People (95.05%)
# Street (89.12%)
# Mode of transport (89.09%)
# Transport (85.13%)
# Vehicle (84.69%)
# Snapshot (84.11%)
# Urban area (80.29%)
# Infrastructure (73.14%)
# Road (72.74%)
# Pedestrian (68.90%)
# from google.cloud import vision

# sample face detection
from google.cloud import vision

uri_base = 'gs://cloud-vision-codelab'
pics = ('face_surprise.jpg', 'face_no_surprise.png')

client = vision.ImageAnnotatorClient()
image = vision.types.Image()

for pic in pics:
    image.source.image_uri = f'{uri_base}/{pic}'
    response = client.face_detection(image=image)

    print('=' * 79)
    print(f'File: {pic}')
    for face in response.face_annotations:
        likelihood = vision.enums.Likelihood(face.surprise_likelihood)
        vertices = [f'({v.x},{v.y})' for v in face.bounding_poly.vertices]
        print(f'Face surprised: {likelihood.name}')
        print(f'Face bounds: {",".join(vertices)}')

# ===============================================================================
# File: face_surprise.jpg
# Face surprised: LIKELY
# Face bounds: (93,425),(520,425),(520,922),(93,922)
# ===============================================================================
# File: face_no_surprise.png
# Face surprised: VERY_UNLIKELY
# Face bounds: (120,0),(334,0),(334,198),(120,198)
