from typing import Any

from django.template import loader

from infrastructure.email_services.work_email_service.context_processor.context_processor import (
    get_work_email_context_processor,
)
from infrastructure.email_services.work_email_service.context_processor.context_processor_interface import (
    WorkEmailContextProcessorInterface,
)
from infrastructure.email_services.work_email_service.template_generator.template_generator_interface import (
    WorkEmailTemplateGeneratorInterface,
)


class WorkEmailTemplateGenerator(WorkEmailTemplateGeneratorInterface):
    def __init__(self, context_processor: WorkEmailContextProcessorInterface) -> None:
        self.context_processor = context_processor

    @staticmethod
    def generate_template(template_name: str, context: dict[Any, Any]) -> str:
        return loader.render_to_string(template_name, context, request=None, using=None)

    def generate_success_login_in_admin_template(self, **kwargs) -> str:
        context = self.context_processor.try_login_in_admin(**kwargs)

        return self.generate_template("emails/success_login_in_admin.html", context)

    def generate_cant_login_in_admin_template(self, **kwargs) -> str:
        context = self.context_processor.try_login_in_admin(**kwargs)

        return self.generate_template("emails/error_login_in_admin.html", context)

    def generate_login_in_fake_admin(self, **kwargs) -> str:
        context = self.context_processor.login_in_fake_admin(**kwargs)

        return self.generate_template("emails/login_in_fake_admin.html", context)

    def generate_errror_message(self, **kwargs) -> str:
        context = self.context_processor.error_message(**kwargs)

        return self.generate_template("emails/error_message.html", context)

    def generate_login_code(self, code: int, **kwargs) -> str:
        context = self.context_processor.login_code(code, **kwargs)

        return self.generate_template("emails/login_code.html", context)


def get_work_email_template_generator(
    email_context_processor: WorkEmailContextProcessorInterface = get_work_email_context_processor(),
) -> WorkEmailTemplateGeneratorInterface:
    return WorkEmailTemplateGenerator(email_context_processor)
