from enum import Enum


class Errors(str, Enum):
    incorrect_file_name = "Неккоректное название файла"
    block_with_name_already_exist = "Уже есть блок, привязанный к этому имени"
