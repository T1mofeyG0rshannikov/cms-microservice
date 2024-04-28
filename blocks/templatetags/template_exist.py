from django import template
from django.shortcuts import render

register = template.Library()


@register.simple_tag()
def template_exists(template_name):
    try:
        template.loader.get_template(template_name)
        return True
    except template.TemplateDoesNotExist:
        return False


@register.simple_tag()
def render_block(template_name, block, id):
    return render(request=None, template_name=template_name, context={"block": block.content, "styles": block.styles})
