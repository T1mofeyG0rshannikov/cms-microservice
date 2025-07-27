from application.dto.product import ProductDTO
from infrastructure.persistence.models.catalog.products import Product


class ProductAssembler:
    def get_offers(self, product: Product) -> list[int]:
        return [offer.id for offer in product.offers.all()]

    def get_end_promotion(self, product) -> str:
        offer = product.offers.filter(partner_program="Пригласи друга").first()

        if offer:
            return offer.get_end_promotion.strftime("%d.%m.%Y")

        for offer in product.offers.all():
            if offer.end_promotion:
                return offer.get_end_promotion.strftime("%d.%m.%Y")

        return "Бессрочно"

    def process(self, product: Product) -> ProductDTO:
        product = ProductDTO.process(
            product,
            name=f"{product.name} ({product.category})",
            organization=product.organization.name,
            image=product.cover.url,
            offers=self.get_offers(product),
            end_promotion=self.get_end_promotion(product),
        )
        return product


def get_product_dto_builder() -> ProductAssembler:
    return ProductAssembler()
