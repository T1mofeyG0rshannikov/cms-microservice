from enum import Enum


class Messages(str, Enum):
    sent_message_to_reset_password = "Вам на почту пришло письмо с ссылкой для сброса пароля"
