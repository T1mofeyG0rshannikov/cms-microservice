from web.account.exc_handler import referrals_exception_handler
from web.emails.exc_handler import email_exception_handler

exceptions_handlers = [referrals_exception_handler, email_exception_handler]


def my_exception_handler(exc, context):
    for handler in exceptions_handlers:
        error_response = handler(exc)
        if error_response:
            return error_response
