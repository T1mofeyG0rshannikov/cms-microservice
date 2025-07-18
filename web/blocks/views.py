import json

from django.db.utils import IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from application.services.pages_service import get_page_service
from application.usecases.public.catalog_page import get_catalog_page
from web.blocks.serializers import PageSerializer
from domain.page_blocks.page_service_interface import PageServiceInterface
from infrastructure.files.files import find_class_in_directory
from infrastructure.persistence.repositories.page_repository import get_page_repository


class PageView(View):
    def get(self, request):
        page_repository = get_page_repository()
        page_url = request.GET.get("url")
        print(page_url)
        page = page_repository.get(url=None)
        print(page)

        return JsonResponse({"page": PageSerializer(page).data})


class GetCatalogPageView(View):
    def get(self, request):
        slug = request.GET.get("url")
        user_is_authenticated = request.user.is_authenticated
        page = get_catalog_page(slug=slug, user_is_authenticated=user_is_authenticated)
        return JsonResponse({"page": PageSerializer(page).data})

@method_decorator(csrf_exempt, name="dispatch")
class ClonePage(View):
    def post(self, request: HttpRequest, page_service: PageServiceInterface = get_page_service()) -> HttpResponse:
        data = json.loads(request.body)
        page_id = data.get("page_id")

        page_service.clone_page(page_id)

        return HttpResponse(status=201)


@method_decorator(csrf_exempt, name="dispatch")
class CloneBlock(View):
    def post(self, request):
        data = json.loads(request.body)
        block_id = data.get("block_id")
        block_class = data.get("block_class")

        block_class = find_class_in_directory("blocks/models", block_class)

        block = block_class.objects.get(id=block_id)

        related_objects_to_copy = []
        relations_to_set = {}
        # Iterate through all the fields in the parent object looking for related fields
        for field in block._meta.get_fields():
            if field.one_to_many:
                # One to many fields are backward relationships where many child objects are related to the
                # parent (i.e. SelectedPhrases). Enumerate them and save a list so we can copy them after
                # duplicating our parent object.
                print(f"Found a one-to-many field: {field.name}")

                # 'field' is a ManyToOneRel which is not iterable, we need to get the object attribute itself
                if hasattr(block, field.name):
                    related_object_manager = getattr(block, field.name)
                    related_objects = list(related_object_manager.all())
                    if related_objects:
                        print(f" - {len(related_objects)} related objects to copy")
                        related_objects_to_copy += related_objects

            elif field.many_to_one:
                # In testing so far, these relationships are preserved when the parent object is copied,
                # so they don't need to be copied separately.
                print(f"Found a many-to-one field: {field.name}")

            elif field.many_to_many:
                # Many to many fields are relationships where many parent objects can be related to many
                # child objects. Because of this the child objects don't need to be copied when we copy
                # the parent, we just need to re-create the relationship to them on the copied parent.
                print(f"Found a many-to-many field: {field.name}")
                related_object_manager = getattr(block, field.name)
                relations = list(related_object_manager.all())
                if relations:
                    print(f" - {len(relations)} relations to set")
                    relations_to_set[field.name] = relations

        # Duplicate the parent object
        block.pk = None
        try:
            block.save()
        except IntegrityError:
            name = block.name + "(1)"
            block.name = name
            block.save()

        print(f"Copied parent object ({str(block)})")

        # Copy the one-to-many child objects and relate them to the copied parent
        for related_object in related_objects_to_copy:
            # Iterate through the fields in the related object to find the one that relates to the
            # parent model (I feel like there might be an easier way to get at this).
            for related_object_field in related_object._meta.fields:
                if related_object_field.related_model == block.__class__:
                    # If the related_model on this field matches the parent object's class, perform the
                    # copy of the child object and set this field to the parent object, creating the
                    # new child -> parent relationship.
                    related_object.pk = None
                    setattr(related_object, related_object_field.name, block)
                    related_object.save()

                    text = str(related_object)
                    text = (text[:40] + "..") if len(text) > 40 else text
                    print(f"|- Copied child object ({text})")

        # Set the many-to-many relations on the copied parent
        for field_name, relations in relations_to_set.items():
            # Get the field by name and set the relations, creating the new relationships
            field = getattr(block, field_name)
            field.set(relations)
            text_relations = []
            for relation in relations:
                text_relations.append(str(relation))
            print(f"|- Set {len(relations)} many-to-many relations on {field_name} {text_relations}")

        return HttpResponse(status=201)
