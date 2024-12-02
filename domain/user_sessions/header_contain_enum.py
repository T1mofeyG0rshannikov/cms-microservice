from enum import StrEnum


class HeaderContainEnum(StrEnum):
    contain = "Содержит"
    have = "Присутствует"
    not_contain = "Не содержит"
    not_match = "Не совпадает"
    match = "Совпадает"
    miss = "Отсутствует"