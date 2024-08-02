from enum import Enum


class Errors(str, Enum):
    incorrect_file_name = "Неккоректное название файла"
    block_with_name_already_exist = "Уже есть блок, привязанный к этому имени"
    template_doesnt_exist = "Нет такого html файла"
    expired_set_password_token = "Срок действия токена для ввода пароля истёк"
    wrong_confirm_email_link = "Проверочная ссылка некорректная или истек срок ее действия. Запросите проверку email еще раз в личном кабинете."
    wrong_reset_password_link = "Ссылка для восстановления пароля некорректная или истек срок ее действия. Запросите восстановление пароля еще раз."


class UserErrors(str, Enum):
    username_with_phone_alredy_exists = "Пользователь с таким телефоном уже существует"
    username_with_email_alredy_exists = "Пользователь с такой почтой уже существует"
    incorrect_phone = "Неверный номер телефона"
    incorrect_login = "Неверный логин"
    incorrect_password = "Неверный пароль"
    user_by_phone_not_found = "Нет пользователя с таким телефоном"
    user_by_email_not_found = "Пользователь с таким email не существует"
    login_first = "Сначала войдите в аккаунт"
    you_already_have_your_own_website = "вы уже имеете свой сайт"
    something_went_wrong = "что-то пошло не так, попробуйте позже"
