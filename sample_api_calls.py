#!/usr/bin/env python

from google.cloud import vision

# sample label detection
image_uri = 'https://iiif.princeton.edu/loris/figgy_prod/cb%2F1f%2F3c%2Fcb1f3ca1536c4c7388f4f610cd0659a6%2Fintermediate_file.jp2/full/1200,/0/default.jpg'

client = vision.ImageAnnotatorClient()
# image = vision.types.Image()
# image.source.image_uri = image_uri

with open('abc-jingle1.jpg', 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.label_detection(image=image)

objects = client.object_localization(image=image).localized_object_annotations
print('Number of objects found: {}'.format(len(objects)))
for object_ in objects:
    print('\n{} (confidence: {})'.format(object_.name, object_.score))
    print('Normalized bounding polygon vertices: ')
    for vertex in object_.bounding_poly.normalized_vertices:
        print(' - ({}, {})'.format(vertex.x, vertex.y))

print()
print('Labels (and confidence score):')
print('=' * 79)
for label in response.label_annotations:
    print(f'{label.description} ({label.score*100.:.2f}%)')

response = client.face_detection(image=image)
faces = response.face_annotations

# Names of likelihood from google.cloud.vision.enums
likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE','LIKELY', 'VERY_LIKELY')
print('Faces:')

for face in faces:
    print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
    print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
    print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

    vertices = (['({},{})'.format(vertex.x, vertex.y)
        for vertex in face.bounding_poly.vertices])

    print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

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
