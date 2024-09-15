from blocks.template_exist import is_template_exists
from django import template

register = template.Library()


@register.simple_tag()
def template_exists(template_name: str) -> bool:
    return is_template_exists(template_name)
