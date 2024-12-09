from PIL import Image

from application.texts.errors import ErrorsMessages, SiteErrorsMessages
from domain.common.exceptons import InvalidFileExtension, ToLagreFile, ToLargeImageSize
from domain.common.screen import FileInterface
from domain.domains.exceptions import InvalidSiteAddress, InvalidSiteName
from domain.domains.site_validator import SiteValidatorInterface


class SiteValidator(SiteValidatorInterface):
    def valid_name(self, name: str) -> str:
        if not (4 <= len(name) <= 16):
            raise InvalidSiteName(SiteErrorsMessages.invalid_site_name)

        return name

    def valid_site(self, site: str) -> str:
        if len(site) < 4:
            raise InvalidSiteAddress(SiteErrorsMessages.to_short_address)

        if not (site.isalnum() and all(c.isascii() for c in site)):
            raise InvalidSiteAddress(SiteErrorsMessages.invalid_literal)

        return site

    def valid_logo(self, logo: FileInterface) -> FileInterface:
        if logo:
            if logo.size > 204800:
                raise ToLagreFile(ErrorsMessages.to_large_file)

            file_extension = logo.name.split(".")[-1].lower()
            if file_extension not in ["png", "gif"]:
                raise InvalidFileExtension(ErrorsMessages.wrong_image_format)

            try:
                img = Image.open(logo)
                width, height = img.size
                if height > 200 or width > 500:
                    raise ToLargeImageSize(ErrorsMessages.to_large_image_size)

            except Exception:
                pass

        return logo


def get_site_validator() -> SiteValidatorInterface:
    return SiteValidator()
