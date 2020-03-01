import os
import sys

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BAD_REQUEST = 400
SUCCESS = 200

# 'content' is base-64-encoded image data.
@app.route("/submit-image", methods=["POST"])
def get_prediction(content, project_id, model_id):
    prediction_client = automl_v1beta1.PredictionServiceClient()

    name = "projects/{}/locations/us-central1/models/{}".format(project_id, model_id)
    payload = {"image": {"image_bytes": content}}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned


if __name__ == "__main__":
    file_path = sys.argv[1]
    project_id = sys.argv[2]
    model_id = sys.argv[3]
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
        os.getcwd(), "slohacks.json"
    )

    with open(file_path, "rb") as ff:
        content = ff.read()
    print(type(content))
    print(get_prediction(content, project_id, model_id))
