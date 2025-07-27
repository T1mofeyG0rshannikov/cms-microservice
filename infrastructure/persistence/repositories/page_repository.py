from typing import List

from django.db.models import Model, Q

from application.mappers.page import from_orm_to_page
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


class PageRepository(PageRepositoryInterface):
    def get_catalog_block(self, slug: str) -> CatalogBlock | None:
        try:
            return CatalogBlock.objects.select_related("template").get(product_type__slug=slug)
        except CatalogBlock.DoesNotExist:
            return None

    def get(self, id: int | None = None, url: str | None = None) -> PageInterface | None:
        query = Q()
        if id:
            query &= Q(id=id)
        else:
            query &= Q(url=url)

        try:
            page = Page.objects.get(query)
            return from_orm_to_page(page=page, blocks=self.__get_page_blocks(page))

        except Page.DoesNotExist:
            return None

    def __get_page_blocks(self, page: BasePageModel) -> list[BaseBlock]:
        BLOCKCLASSES = {Page: Block, CatalogPageTemplate: CatalogPageBlock, Landing: LandingBlock}

        try:
            block_class = BLOCKCLASSES[type(page)]
        except KeyError:
            raise ValueError("page_model must be 'Page', 'CatalogPageTemplate' or 'Landing' instance")

        blocks = block_class.objects.filter(page=page).select_related("content_type").order_by("my_order")
        return [
            block.content_type.model_class()
            .objects.select_related("template")
            .prefetch_related("styles")
            .get(id=block.block_id)
            for block in blocks
        ]

    def get_catalog_page_template(self) -> tuple[PageInterface, list[BaseBlock]]:
        page = CatalogPageTemplate.objects.first()
        return page, self.__get_page_blocks(page)

    def get_catalog_cover(self, slug: str) -> PageBlockInterface:
        return Cover.objects.select_related("template").get(producttype__slug=slug)

    def get_landing(self, url: str) -> PageInterface:
        page = Landing.objects.get(url=url)
        return from_orm_to_page(page=page, blocks=self.__get_page_blocks(page))

    def get_landing_logo(self, url: str) -> ImageInterface | None:
        try:
            landing = Landing.objects.get(url=url)
        except Landing.DoesNotExist:
            return None

        return landing.logo

    def __clone_obj(self, obj: Model) -> None:
        related_objects_to_copy = []
        relations_to_set = {}

        for field in obj._meta.get_fields():
            if field.one_to_many:
                if hasattr(obj, field.name):
                    related_object_manager = getattr(obj, field.name)
                    related_objects = list(related_object_manager.all())
                    if related_objects:
                        related_objects_to_copy += related_objects

            elif field.many_to_many:
                related_object_manager = getattr(obj, field.name)
                relations = list(related_object_manager.all())
                if relations:
                    relations_to_set[field.name] = relations

        obj.pk = None
        obj.save()

        for related_object in related_objects_to_copy:
            for related_object_field in related_object._meta.fields:
                if related_object_field.related_model == obj.__class__:
                    related_object.pk = None
                    setattr(related_object, related_object_field.name, obj)
                    related_object.save()

        for field_name, relations in relations_to_set.items():
            field = getattr(obj, field_name)
            field.set(relations)

    def clone_block(self, block_id: int, block_class: BaseBlock) -> None:
        block = block_class.objects.get(id=block_id)
        self.__clone_obj(block)

    def clone_page(self, id: int) -> None:
        page = Page.objects.get(id=id)
        self.__clone_obj(page)


def get_page_repository() -> PageRepositoryInterface:
    return PageRepository()
