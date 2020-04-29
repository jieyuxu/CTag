#!/usr/bin/env python

from google.cloud import vision
import io, request

def combine_dict(emotions, labels):
    tag_type = {}
    big_dict = {}
    for l in labels:
        big_dict[l] = labels[l]
        tag_type[l] = 'Label'

    likelihood_name = ['UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY']
    for e in emotions:
        conf_emot = likelihood_name.index(emotions[e])
        big_dict[e] = conf_emot
        tag_type[e] = 'Emotions'

    return big_dict, tag_type

def annotate_img_path(filename):
    emotions = detect_faces(filename)
    labels = detect_labels(filename)

    # print(emotions, labels)
    return combine_dict(emotions, labels)

def annotate_img_bytestream(bytestream):
    emotions = detect_faces_bytestream(bytestream)
    labels = detect_labels_bytestream(bytestream)

    # print(emotions, labels)
    return combine_dict(emotions, labels)

def detect_faces(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    emotions = {}

    for face in faces:
        emotions['anger'] = likelihood_name[face.anger_likelihood]
        emotions['joy'] = likelihood_name[face.joy_likelihood]
        emotions['surprise'] = likelihood_name[face.surprise_likelihood]
        emotions['sorrow'] = likelihood_name[face.sorrow_likelihood]

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return emotions


def detect_faces_bytestream(bytestream):
    client = vision.ImageAnnotatorClient()

    image = vision.types.Image(content=bytestream)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    # print('Faces:')
    emotions = {}
    for face in faces:
        # print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        # print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        # print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        # print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))
        emotions['anger'] = likelihood_name[face.anger_likelihood]
        emotions['joy'] = likelihood_name[face.joy_likelihood]
        emotions['surprise'] = likelihood_name[face.surprise_likelihood]
        emotions['sorrow'] = likelihood_name[face.sorrow_likelihood]

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return emotions


def detect_labels(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations


    label_set = {}
    for label in labels:
        label_set[label.description] = label.score*100

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return label_set


def detect_labels_bytestream(bytestream):
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image(content=bytestream)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    label_set = {}
    for label in labels:
        label_set[label.description] = label.score*100

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return label_set

def detect_web_uri(bytestream):
    """Detects web annotations in the file located in Google Cloud Storage."""
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image(content=bytestream)

    response = client.web_detection(image=image)
    annotations = response.web_detection

    # best_guess_labels = set()

    # if annotations.best_guess_labels:
    #     for label in annotations.best_guess_labels:
    #         print('\nBest guess label: {}'.format(label.label))
    #         best_guess_labels.add(label.label)

    # if annotations.pages_with_matching_images:
    #     print('\n{} Pages with matching images found:'.format(
    #         len(annotations.pages_with_matching_images)))

    #     for page in annotations.pages_with_matching_images:
    #         print('\n\tPage url   : {}'.format(page.url))

    #         if page.full_matching_images:
    #             print('\t{} Full Matches found: '.format(
    #                    len(page.full_matching_images)))

    #             for image in page.full_matching_images:
    #                 print('\t\tImage url  : {}'.format(image.url))

    #         if page.partial_matching_images:
    #             print('\t{} Partial Matches found: '.format(
    #                    len(page.partial_matching_images)))

    #             for image in page.partial_matching_images:
    #                 print('\t\tImage url  : {}'.format(image.url))

    # maps description to score
    # best_guess_description = dict()

    # if annotations.web_entities:
    #     print('\n{} Web entities found: '.format(
    #         len(annotations.web_entities)))

    #     for entity in annotations.web_entities:
    #         best_guess_description[entity.description] = entity.score
    #         print('\n\tScore      : {}'.format(entity.score))
    #         print(u'\tDescription: {}'.format(entity.description))

    similar_images = set()
    if annotations.visually_similar_images:
        print('\n{} visually similar images found:\n'.format(
            len(annotations.visually_similar_images)))

        for image in annotations.visually_similar_images:
            similar_images.add(image.url)
            print('\tImage url    : {}'.format(image.url))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    return similar_images
