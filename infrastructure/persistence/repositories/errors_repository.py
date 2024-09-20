from domain.logging.error import ErrorLogRepositoryInterface
from web.site_tests.models import Error


class ErrorsRepository(ErrorLogRepositoryInterface):
    @staticmethod
    def create_error_log(**kwargs) -> None:
        Error.objects.create(**kwargs)


def get_errors_repository() -> ErrorLogRepositoryInterface:
    return ErrorsRepository()
