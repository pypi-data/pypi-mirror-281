# -*- coding: utf-8 -*-
import json


def load_model(model_path):
    from tensorflow import keras

    return keras.models.load_model(model_path)


def dump_model(model, path):
    model.save(path)


def get_model_structure(model_obj):
    ml_model_class = json.loads(model_obj.to_json())
    ml_model_class["class"] = str(model_obj.__class__)[8:-2:]
    return json.dumps(ml_model_class)
