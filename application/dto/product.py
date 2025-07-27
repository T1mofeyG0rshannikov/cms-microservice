from dataclasses import dataclass

from application.dto.blocks import BaseDTO


@dataclass
class ProductDTO(BaseDTO):
    id: int
    name: str
    organization: str
    image: str
    partner_annotation: str
    offers: list[int]
    end_promotion: str


@dataclass
class OrganizationDTO(BaseDTO):
    id: int
    name: str
