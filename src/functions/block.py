from enum import Enum
import re
from src.regex_patterns import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered_list"

# Split markdown text to a list of text blocks
def markdown_to_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    strings: list[str] = text.split("\n\n")
    for s in strings:
        if s is not None and s != "":
            blocks.append(s.strip())
    return blocks

# Determine the type of markdown a block is, defaulting to paragraph
def block_to_block_type(block: str) -> BlockType:
    if re.match(HEADER_PATTERN, block) is not None:
        return BlockType.HEADING
    elif re.match(CODE_PATTERN, block) is not None:
        return BlockType.CODE
    elif re.match(UNORDERED_LIST_PATTERN, block) is not None:
        return BlockType.UNORDERED_LIST
    elif re.match(ORDERED_LIST_PATTERN, block) is not None:
        line_num: int = 1
        lines: list[str] = block.strip().splitlines()
        for s in lines:
            if s.startswith(f"{line_num}. "):
                line_num += 1
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    elif re.match(QUOTED_PATTERN, block) is not None:
        return BlockType.QUOTE
    else:
        return BlockType.PARAGRAPH