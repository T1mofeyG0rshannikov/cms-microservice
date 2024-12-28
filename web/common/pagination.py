from collections.abc import Iterable
from typing import Any

from django.core.paginator import Paginator
from django.http import HttpRequest


class Pagination:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def paginate(
        self, objects: Iterable[Any], objects_context_name: str, serializer_class=None, serializer_context=None
    ) -> dict[str, Any]:
        page_number = int(self.request.GET.get("page", 1))
        page_size = int(self.request.GET.get("page_size", 10))

        context = {"count": len(objects)}  # type: ignore

        paginator = Paginator(objects, page_size)
        objects_pagination = paginator.get_page(page_number)

        context["current_page"] = objects_pagination.number
        context["total_pages"] = objects_pagination.paginator.num_pages

        if serializer_class:
            context[objects_context_name] = serializer_class(
                objects_pagination.object_list, context=serializer_context, many=True
            ).data
        else:
            context[objects_context_name] = objects_pagination.object_list

        return context
