import pickle
from flask import Flask
from flask import request
import numpy as np
import json


def load_classifier():
    with open("iris_classifier", "rb") as f:
        clf = pickle.load(f)

    with open("feature_names", "rb") as f:
        features = pickle.load(f)

    return clf, features


app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def inference():
    clf, features = load_classifier()
    class_name = ['setosa', 'versicolor', 'virginica']
    resp = {}

    content = request.json
    if not isinstance(content, list):
        content = [content]

    for i, elem in enumerate(content):
        test_data = []
        for feature in features:
            test_data.append(elem[feature])
        species = clf.predict(np.array([test_data]))
        resp.update({"input {}".format(i):class_name[species[0]]})

    return json.dumps(resp, indent=4)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
