from .models.common import Page


def clone_page(page_id):
    page = Page.objects.get(id=page_id)
    blocks = page.blocks.all()
    print(blocks)

    page.pk = None

    page.save()

    for block in blocks:
        #  print(block, block.id)
        block.pk = None
        block.page = page
        block.save()
    #    print(block.id)


#  print(page)
