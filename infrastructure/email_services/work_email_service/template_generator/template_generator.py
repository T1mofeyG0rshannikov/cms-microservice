from typing import Any

from django.template import loader

from infrastructure.admin.admin_settings import AdminSettings, get_admin_settings
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
    def __init__(self, context_processor: WorkEmailContextProcessorInterface, admin_settings: AdminSettings) -> None:
        self.context_processor = context_processor
        self.admin_settings = admin_settings

    @staticmethod
    def generate_template(template_name: str, context: dict[str, Any]) -> str:
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

    def generate_feedback_email(
        self, username: str, email: str, phone: str, message: str, site_name: str, site_domain: str, user_id: int = None
    ) -> str:
        if user_id:
            user_link = f"https://{self.admin_settings.admin_domain}/{self.admin_settings.admin_url}/user/user/{user_id}/change/"
        else:
            user_link = None

        print(user_id)
        print(user_link)

        return self.generate_template(
            "emails/feedback.html",
            {
                "username": username,
                "email": email,
                "phone": phone,
                "message": message,
                "site_name": site_name,
                "site_domain": site_domain,
                "user_link": user_link,
            },
        )


def get_work_email_template_generator(
    email_context_processor: WorkEmailContextProcessorInterface = get_work_email_context_processor(),
    admin_settings: AdminSettings = get_admin_settings(),
) -> WorkEmailTemplateGeneratorInterface:
    return WorkEmailTemplateGenerator(email_context_processor, admin_settings)
