from blocks.models.common import BaseBlock


def get_block(blocks_name):
    blocks = [
        f.field.model.objects.filter(block_relation=blocks_name).first()
        for f in blocks_name._meta.get_fields()
        if (f.one_to_many or f.one_to_one) and isinstance(f.field.model.objects.first(), BaseBlock)
    ]

    if blocks:
        block = [block for block in blocks if block is not None][0]
    else:
        block = None

    return block
