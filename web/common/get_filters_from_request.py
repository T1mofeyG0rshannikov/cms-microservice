from dataclasses import fields
from typing import Type, TypeVar

from django.http import HttpRequest

T = TypeVar("T")


def get_db_filters_from_request(filters_interface: type[T], request: HttpRequest) -> T:
    data = {}
    for field in fields(filters_interface):
        data[field.name] = request.GET.get(field.name)

    return filters_interface(**data)
