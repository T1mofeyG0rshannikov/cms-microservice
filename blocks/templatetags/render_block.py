from django import template
from django.shortcuts import render
from django.template import loader

register = template.Library()


@register.simple_tag()
def render_block(template_name, block, id):
    content = loader.render_to_string(
        template_name, context={"block": block["content"], "styles": block["styles"]}, request=None
    )

    print(
        render(
            request=None, template_name=template_name, context={"block": block["content"], "styles": block["styles"]}
        )
    )
    return content
