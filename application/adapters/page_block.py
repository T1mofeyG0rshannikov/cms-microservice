from domain.page_blocks.entities.base_block import (
    BaseBlockInterface,
    BlockStyles,
    PageBlockInterface,
)
from infrastructure.persistence.models.blocks.common import BaseBlock
from infrastructure.public.template_settings import (
    TemplateSettings,
    get_template_settings,
)


class BlockAdapter:
    def __init__(self, template_config: TemplateSettings) -> None:
        self.config = template_config

    def __call__(self, block: BaseBlock) -> PageBlockInterface:
        if block is not None:
            block.template.file = self.config.blocks_templates_folder + "/" + block.template.file

        return PageBlockInterface(content=block, styles=self.get_styles(block))

    def get_styles(self, block: BaseBlockInterface) -> BlockStyles:
        if not block:
            return False

        return block.get_styles()


def get_block_adapter(template_config=get_template_settings()) -> BlockAdapter:
    return BlockAdapter(template_config)
