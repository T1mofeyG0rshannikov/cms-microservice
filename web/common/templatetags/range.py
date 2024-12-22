from django import template

register = template.Library()


@register.filter
def create_range(value, start_index=0):
    return range(start_index, value + start_index)


@register.filter(name="convert_to_int")
def convert_to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0
