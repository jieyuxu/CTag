import sys

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

# 'content' is base-64-encoded image data.
def get_prediction(content, project_id, model_id):
    prediction_client = automl_v1beta1.PredictionServiceClient()

    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned

def custom_tagger(bytestream):
    project_id = '1014211948718'
    model_id = 'ICN8010175304813248512'

    tags = {}
    request = get_prediction(bytestream, project_id, model_id)
    for result in request.payload:
        t = result.display_name
        s = result.classification.score
        # print("Predicted class name: {}".format(result.display_name))
        # print(result.classification.score)
        tags[t] = s

    return tags
