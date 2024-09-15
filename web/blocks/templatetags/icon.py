import xml.etree.ElementTree as ET

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def icon(file, fill="#000000"):
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(file.file)
    root = tree.getroot()
    root.set("fill", fill)
    svg = ET.tostring(root, encoding="unicode", method="html")

    return mark_safe(svg)
