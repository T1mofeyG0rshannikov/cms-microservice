from typing import List

from application.usecases.public.get_page.strategies import (
    GetCatalogPageStrategy,
    GetDefaultPageStrategy,
    GetPageStrategy,
)
from domain.page_blocks.entities.page import PageInterface
from domain.page_blocks.exceptions import PageNotFoundError
from domain.page_blocks.page_repository import PageRepositoryInterface
from infrastructure.persistence.repositories.page_repository import get_page_repository


class GetPage:
    def __init__(
        self,
        page_repository: PageRepositoryInterface,
    ) -> None:
        self._strategies: list[GetPageStrategy] = [
            GetDefaultPageStrategy(page_repository),
            GetCatalogPageStrategy(page_repository),
        ]

    def __call__(self, url: str | None = None, user_is_authenticated: bool = False) -> PageInterface:
        for strategy in self._strategies:
            page = strategy.execute(url=url, user_is_authenticated=user_is_authenticated)

            if page is not None:
                return page

        raise PageNotFoundError


def get_page(
    page_repository: PageRepositoryInterface = get_page_repository(),
) -> GetPage:
    return GetPage(page_repository)
