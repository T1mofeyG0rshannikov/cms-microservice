from django.http import JsonResponse

from domain.user.exceptions import InvalidReferalLevel, InvalidSortedByField


def referrals_exception_handler(exc):
    if isinstance(exc, (InvalidReferalLevel, InvalidSortedByField)):
        return JsonResponse(
            {
                "error": str(exc),
            },
            status=400,
        )
