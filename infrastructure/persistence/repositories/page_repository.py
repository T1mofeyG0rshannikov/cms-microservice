from collections.abc import Iterable

from django.core.cache import cache
from django.db.models import Case, Q, When

from application.mappers.page import from_orm_to_block, from_orm_to_page
from domain.common.screen import ImageInterface
from domain.page_blocks.entities.base_block import PageBlockInterface
from domain.page_blocks.entities.page import PageInterface
from domain.page_blocks.page_repository import PageRepositoryInterface
from infrastructure.persistence.models.blocks.blocks import Cover
from infrastructure.persistence.models.blocks.catalog_block import CatalogBlock
from infrastructure.persistence.models.blocks.common import (
    BaseBlock,
    BasePageModel,
    Block,
    Page,
)
from infrastructure.persistence.models.blocks.landings import Landing, LandingBlock
from infrastructure.persistence.models.catalog.blocks import Block as CatalogPageBlock
from infrastructure.persistence.models.catalog.blocks import CatalogPageTemplate
from infrastructure.persistence.models.common import BlockRelationship


class PageRepository(PageRepositoryInterface):
    def get_catalog_block(self, slug: str) -> PageBlockInterface | None:
        try:
            block = CatalogBlock.objects.select_related("template").get(product_type__slug=slug)
        except CatalogBlock.DoesNotExist:
            return None

        return from_orm_to_block(block)

    def get(self, id: int | None = None, url: str | None = None) -> PageInterface | None:
        query = Q()
        if id:
            query &= Q(id=id)
        else:
            query &= Q(url=url)

        try:
            page = Page.objects.get(query)
        except Page.DoesNotExist:
            return None
        
        return from_orm_to_page(page=page, blocks=self.__get_page_blocks(page))

    def __get_page_blocks(self, page_model: BasePageModel) -> Iterable[BaseBlock]:
        if isinstance(page_model, Page):
            page_block_class = Block

        elif isinstance(page_model, CatalogPageTemplate):
            page_block_class = CatalogPageBlock

        elif isinstance(page_model, Landing):
            page_block_class = LandingBlock

        else:
            raise ValueError("page_model must be 'Page', 'CatalogPageTemplate' or 'Landing' instance")

        block_names = (
            page_block_class.objects.filter(page=page_model).order_by("my_order").values_list("name", flat=True)
        )

        blocks = BlockRelationship.objects.filter(id__in=block_names).order_by(
            Case(*[When(id=id, then=pos) for pos, id in enumerate(block_names)])
        )

        block_models = []
        for block in blocks:
            block_model = (
                block.__getattribute__(block.block_model_name)
                .select_related("template")
                .prefetch_related("styles")
                .first()
            )

            block_models.append(block_model)

        return block_models

    def clone_page(self, id: int) -> None:
        page = Page.objects.get(id=id)

        related_objects_to_copy = []
        relations_to_set = {}

        for field in page._meta.get_fields():
            if field.one_to_many:
                if hasattr(page, field.name):
                    related_object_manager = getattr(page, field.name)
                    related_objects = list(related_object_manager.all())
                    if related_objects:
                        related_objects_to_copy += related_objects

            elif field.many_to_many:
                related_object_manager = getattr(page, field.name)
                relations = list(related_object_manager.all())
                if relations:
                    relations_to_set[field.name] = relations

        page.pk = None
        page.save()

        for related_object in related_objects_to_copy:
            for related_object_field in related_object._meta.fields:
                if related_object_field.related_model == page.__class__:
                    related_object.pk = None
                    setattr(related_object, related_object_field.name, page)
                    related_object.save()

        for field_name, relations in relations_to_set.items():
            field = getattr(page, field_name)
            field.set(relations)

    def get_catalog_page_template(self) -> PageInterface:
        page = CatalogPageTemplate.objects.first()
        return from_orm_to_page(page, blocks=self.__get_page_blocks(page))

    def get_catalog_cover(self, slug: str) -> PageBlockInterface:
        return from_orm_to_block(Cover.objects.select_related("template").get(producttype__slug=slug))

    def get_landing(self, url: str) -> PageInterface:
        page = Landing.objects.get(url=url)
        return from_orm_to_page(page=page, blocks=self.__get_page_blocks(page))

    def get_landing_logo(self, url: str) -> ImageInterface | None:
        try:
            landing = Landing.objects.get(url=url)
        except Landing.DoesNotExist:
            return None

        return landing.logo


def get_page_repository() -> PageRepositoryInterface:
    return PageRepository()
