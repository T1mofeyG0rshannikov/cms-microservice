from django.core.paginator import Paginator


class Pagination:
    def __init__(self, request):
        self.request = request

    def paginate(self, objects, objects_context_name: str, serializer_class=None):
        page_number = int(self.request.GET.get("page", 1))
        page_size = int(self.request.GET.get("page_size", 10))

        context = {"count": len(objects)}

        paginator = Paginator(objects, page_size)
        objects = paginator.get_page(page_number)

        context["current_page"] = objects.number
        context["total_pages"] = objects.paginator.num_pages

        if serializer_class:
            context[objects_context_name] = serializer_class(objects.object_list, many=True).data
        else:
            context[objects_context_name] = objects.object_list

        return context
