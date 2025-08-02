from dataclasses import fields
from typing import List, TypeVar

from django.http import HttpRequest

T = TypeVar("T")


def get_db_filters_from_request(filters_interface: type[T], request: HttpRequest) -> T:
    data = {}
    for field in fields(filters_interface):
        if "list" in str(field.type):
            l = request.GET.getlist(field.name)
            data[field.name] = l if l and l[0] else None
        else:
            data[field.name] = request.GET.get(field.name)

    return filters_interface(**data)
