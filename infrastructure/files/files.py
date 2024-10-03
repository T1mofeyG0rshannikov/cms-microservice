import os
import sys


def get_module_from_dir(directory: str) -> str:
    module = directory.replace("/", ".")
    if module[-1] == ".":
        return module[0:-1]

    return module


def find_class_in_directory(directory: str, class_name):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                module_name = os.path.splitext(file)[0]

                if hasattr(sys.modules[".".join([get_module_from_dir(directory), module_name])], class_name):
                    return getattr(sys.modules[".".join([get_module_from_dir(directory), module_name])], class_name)
