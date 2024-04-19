def get_block(blocks_name):
    block = None
    if blocks_name.navbar_set.first() is not None:
        block = blocks_name.navbar_set.first()

    if blocks_name.exampleblock_set.first() is not None:
        block = blocks_name.exampleblock_set.first()

    return block
