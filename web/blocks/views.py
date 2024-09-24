import json

from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from domain.page_blocks.page_repository import PageRepositoryInterface
from domain.page_blocks.page_service_interface import PageServiceInterface
from infrastructure.files.files import find_class_in_directory
from infrastructure.persistence.repositories.page_repository import get_page_repository
from web.blocks.pages_service.pages_service import get_page_service
from web.blocks.serializers import PageSerializer
from web.domens.views.mixins import SubdomainMixin
from web.settings.models import SiteSettings
from web.user.views.base_user_view import UserFormsView


class IndexPage(SubdomainMixin):
    template_name = "blocks/page.html"
    page_repository: PageRepositoryInterface = get_page_repository()

    def get(self, *args, **kwargs):
        partner_domain = self.domain_service.get_partners_domain_string()

        if self.request.domain == partner_domain and SiteSettings.objects.first().disable_partners_sites:
            return HttpResponse("<h1>Привет :)</h1>")

        if not self.page_repository.get_page_by_url(None):
            return HttpResponseNotFound()

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= UserFormsView.get_context_data()

        page = self.page_repository.get_page_by_url(None)

        serialized_page = PageSerializer(page).data

        context["page"] = serialized_page

        return context


class ShowPage(SubdomainMixin):
    template_name = "blocks/page.html"
    page_repository: PageRepositoryInterface = get_page_repository()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= UserFormsView.get_context_data()

        page = self.page_repository.get_page_by_url(url=kwargs["page_url"])
        serialized_page = PageSerializer(page).data

        context["page"] = serialized_page

        return context


@method_decorator(csrf_exempt, name="dispatch")
class ClonePage(View):
    page_service: PageServiceInterface = get_page_service(get_page_repository())

    def post(self, request):
        data = json.loads(request.body)
        page_id = data.get("page_id")

        self.page_service.clone_page(page_id)

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
