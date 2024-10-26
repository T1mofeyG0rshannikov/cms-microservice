from django import template

register = template.Library()


@register.simple_tag()
def replace(string: str, value_to_replace: str, value: str) -> bool:
    return string.replace(value_to_replace, value)
