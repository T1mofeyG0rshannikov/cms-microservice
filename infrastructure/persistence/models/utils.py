from django.apps import apps
from django.db.models import Model


def get_model_class_by_str(class_name: str) -> Model:
    for model in apps.get_models():
        if model.__name__ == class_name:
            return model
