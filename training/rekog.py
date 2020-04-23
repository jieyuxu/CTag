#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3

def detect_labels(photo):

    client=boto3.client('rekognition')

    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})

    # print('Detected labels in ' + photo)
    labels = []
    for label in response['Labels']:
        # print (label['Name'] + ' : ' + str(label['Confidence']))
        labels.append(label['Name'])
    return labels

# def detect_faces(photo):
#
#     client=boto3.client('rekognition')
#
#     with open(photo, 'rb') as image:
#         response = client.detect_faces(Image={'Bytes': image.read()})
#
#     print(response)
#     print('Detected faces for ' + photo)
#     # for faceDetail in response['FaceDetails']:
#         # print(faceDetail)
#         # print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
#         # #       + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
#         # print('Here are the other attributes:')
#         # print(json.dumps(faceDetail, indent=4, sort_keys=True))
#     return len(response['FaceDetails'])
#

def main():
    photo='try.jpg'

    label=detect_labels(photo)
    print(label)
    # face_count=detect_faces(photo)
    # print("Labels detected: " + str(label_count))
    # print("Faces detected: " + str(face_count))



if __name__ == "__main__":
    main()
