from styles.models.styles.styles import BaseCustomStyles


def get_custom_styles(block):
    styles = [
        f.field.model.objects.filter(block=block.id).first()
        for f in block._meta.get_fields()
        if (f.one_to_many or f.one_to_one) and isinstance(f.field.model.objects.first(), BaseCustomStyles)
    ]

    if styles:
        style = [style for style in styles if style is not None][0]
    else:
        style = None

    return style
