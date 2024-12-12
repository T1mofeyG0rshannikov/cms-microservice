from enum import StrEnum


class ErrorsMessages(StrEnum):
    incorrect_file_name = "Неккоректное название файла"
    block_with_name_already_exist = "Уже есть блок, привязанный к этому имени"
    template_doesnt_exist = "Нет такого html файла"
    expired_set_password_token = "Срок действия токена для ввода пароля истёк"
    wrong_confirm_email_link = "Проверочная ссылка некорректная или истек срок ее действия. Запросите проверку email еще раз в личном кабинете."
    wrong_reset_password_link = "Ссылка для восстановления пароля некорректная или истек срок ее действия. Запросите восстановление пароля еще раз."
    to_large_file = "Изображение не более 200Kb"
    wrong_image_format = "Используйте изображения в PNG или GIF формате"
    to_large_image_size = "Максимальный размер логотипа 500x200px"
    disallowed_host = "Запрещенный домен"
    something_went_wrong = "Что-то пошло не так, повторите попытку чуть позже"
    to_large_file_1mb = "Изображение должно быть не более 1Mb"


class UserErrorsMessages(StrEnum):
    user_with_phone_alredy_exists = "Пользователь с таким телефоном уже существует"
    user_with_email_alredy_exists = "Пользователь с такой почтой уже существует"
    incorrect_phone = "Неверный номер телефона"
    incorrect_login = "Неверный логин"
    incorrect_password = "Неверный пароль"
    user_by_phone_not_found = "Нет пользователя с таким телефоном"
    user_by_email_not_found = "Пользователь с таким email не существует"
    login_first = "Сначала войдите в аккаунт"
    you_already_have_your_own_website = "вы уже имеете свой сайт"
    something_went_wrong = "что-то пошло не так, попробуйте позже"
    user_does_not_exist = "пользователь не найден"
    insufficient_permissions = "Недостаточно прав"
    to_short_password = "Минимум 6 латинских букв и цифр"
    passwords_dont_match = "Пароли не совпадают"
    wrong_code = "Неверный код"


class SiteErrorsMessages(StrEnum):
    address_already_exists = "Такой адрес уже существует"
    invalid_site_name = "Название от 4 до 16 символов"
    to_short_address = "Длина адреса не менее 4 символов"
    invalid_literal = "Можно использовать только латинские буквы и цифры"
