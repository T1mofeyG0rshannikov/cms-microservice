from typing import Any

from domain.domains.domain_repository import DomainRepositoryInterface


class ChangeSite:
    def __init__(self, repository: DomainRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, fields: dict[str, Any], user_id: int):
        fields["domain_id"] = fields["domain"]
        del fields["domain"]

        fields["subdomain"] = fields.get("site")
        del fields["site"]
        fields["font_id"] = fields.get("font")
        del fields["font"]

        fields["logo_width"] = int(260 * (fields["logo_size"] / 100))
        del fields["logo_size"]

        self.repository.update_or_create_user_site(**fields, user_id=user_id)
