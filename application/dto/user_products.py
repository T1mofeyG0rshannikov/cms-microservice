from dataclasses import dataclass


@dataclass
class DeleteProductResponse:
    product_name: str | None
