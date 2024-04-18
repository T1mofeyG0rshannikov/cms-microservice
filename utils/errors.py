from enum import Enum


class Errors(str, Enum):
    incorrect_file_name = "Неккоректное название файла"
    component_with_name_already_exist = "Уже есть компонент, привязанный к этому имени"
