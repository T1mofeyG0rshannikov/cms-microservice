from django import template

from blocks.template_exist import is_template_exists

register = template.Library()


@register.simple_tag()
def template_exists(template_name: str) -> bool:
    return is_template_exists(template_name)
