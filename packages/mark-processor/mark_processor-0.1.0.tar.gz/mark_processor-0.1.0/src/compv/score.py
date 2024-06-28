import os
import json
import numpy as np
from tensorflow.keras.models import load_model
from evaluation_metrics import f1, iou
from azureml.core.model import Model

def init():
    global model
    model_path = Model.get_model_path('primary_model')
    model = load_model(model_path, custom_objects={'f1': f1, 'iou': iou})

def run(data):
    try:
        input_data = np.array(json.loads(data)['data'])
        predictions = model.predict(input_data)
        return json.dumps({"predictions": predictions.tolist()})
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})
