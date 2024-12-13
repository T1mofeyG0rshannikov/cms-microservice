from smsaero import SmsAero

from application.sms_service_interface import SMSServiceInterface
from infrastructure.sms_service.config import SMSAeroConfig, get_sms_config


class SMSService(SMSServiceInterface):
    def __init__(self, config: SMSAeroConfig) -> None:
        self.config = config

    def confirm_phone_code(self, site_name: str, phone: int, code: str) -> None:
        api = SmsAero(self.config.sms_email, self.config.sms_api_key)

        return api.send_sms(phone, f"""{site_name}. Код для подтверждения телефона: {code}""")


def get_sms_service(config: SMSAeroConfig = get_sms_config()) -> SMSAeroConfig:
    return SMSService(config)
