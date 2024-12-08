from enum import StrEnum


class UserActions(StrEnum):
    opened_product_description = "Открыл описание продукта"
    opened_password_change = "Открыл изменение пароля"
    set_password = "Установил пароль"
    changed_profile_data = "Изменил данные профиля"
    changed_password = "Изменил пароль"
    opened_profile_data = "Открыл данные профиля"
    opened_site_settings = "Открыл настройку партнерского сайта"
    opened_products_list = "Открыл список продуктов"
