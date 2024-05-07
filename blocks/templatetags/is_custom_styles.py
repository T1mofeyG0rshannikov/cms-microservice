import xml.etree.ElementTree as ET

from django import template

from styles.models.styles.base_custom_styles import BaseCustomStyles

register = template.Library()


@register.simple_tag()
def template_exists(template_name):
    try:
        template.loader.get_template(template_name)
        return True
    except template.TemplateDoesNotExist:
        return False


@register.simple_tag()
def is_custom_styles(block):
    return isinstance(block, BaseCustomStyles)


# ICON_DIR = "/path/to/your/icons/"


@register.simple_tag
def icon(file, fill="#000000"):
    """Inlines a SVG icon from linkcube/src/core/assets/templates/core.assets/icon

    Example usage:
        {% icon 'face' 'std-icon menu-icon' 32 '#ff0000' %}
    Parameter: file_name
        Name of the icon file excluded the .svg extention.
    Parameter: class_str
        Adds these class names, use "foo bar" to add multiple class names.
    Parameter: size
        An integer value that is applied in pixels as the width and height to
        the root element.
        The material.io icons are by default 24px x 24px.
    Parameter: fill
        Sets the fill color of the root element.
    Returns:
        XML to be inlined, i.e.:
        <svg width="..." height="..." fill="...">...</svg>
    """
    # path = f'{ICON_DIR}/{file_name}.svg'
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    # tree = ET.parse(path)
    #  root = tree.getroot()
    # root.set('class', class_str)
    # #root.set('width', f'{size}px')
    # root.set('height', f'{size}px')
    #  root.set('fill', fill)
    print(file)
    # svg = ET.tostring(root, encoding="unicode", method="html")
    # return mark_safe(svg)
