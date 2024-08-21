from django import template

register = template.Library()


def is_template_exists(template_name: str) -> bool:
    if not template_name:
        return False

    try:
        template.loader.get_template(template_name)
        return True
    except template.TemplateDoesNotExist:
        return False
