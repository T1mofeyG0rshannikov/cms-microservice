from dataclasses import dataclass
from typing import Any

from ckeditor.fields import RichTextField
from django.db import models


@dataclass
class BaseDTO:
    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        filtered_data = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**filtered_data)

    @classmethod
    def process(cls, obj: models.Model, **kwargs):
        data = {**kwargs}
        for field in obj._meta.fields:
            if isinstance(
                field,
                (
                    models.CharField,
                    RichTextField,
                    models.IntegerField,
                    models.BooleanField,
                    models.DateTimeField,
                    models.DateField,
                    models.TextField,
                ),
            ):
                data[field.name] = getattr(obj, field.name)
            elif isinstance(field, models.ImageField):
                data[field.name] = getattr(obj, field.name).url
            elif isinstance(field, models.DateTimeField):
                data[field.name] = getattr(obj, field.name)

        return cls.from_dict(data)
