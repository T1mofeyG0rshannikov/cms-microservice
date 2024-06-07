"""from blocks.models.catalog_block import CatalogBlock
from blocks.models.common import Template


def create_catalog_block(product_type):
    catalog_template = Template.objects.get(file="catalog.html")
    CatalogBlock.objects.create(name=f"Каталог ({product_type.name})",product_type=product_type, template=catalog_template)"""
