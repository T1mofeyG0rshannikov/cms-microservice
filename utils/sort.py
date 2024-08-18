from typing import Any


def sort_list_by_attr(objects: list[Any], sorted_by: str) -> list[Any]:
    reverse = False

    if sorted_by[0] == "-":
        sorted_by = sorted_by[1::]
        reverse = True

    for obj in objects:
        if not hasattr(obj, sorted_by):
            raise ValueError(f"Object '{type(obj).__name__}' has no attr '{sorted_by}'")

    return sorted(objects, key=lambda x: getattr(x, sorted_by), reverse=reverse)
