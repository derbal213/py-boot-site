from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered_list"

HEADER_REGEX = r'^#{1,6} \w*'
CODE_REGEX = r'^`{3}[\s\S]*`{3}$'
UNORDERED_LIST_REGEX = r'^(?:- .*\n?)+$'
ORDERED_LIST_REGEX = r'^(?:\d\. .*\n?)+$'
QUOTED_REGEX = r'^(?:>.*\n?)+$'

def markdown_to_blocks(text):
    blocks = []
    strings = text.split("\n\n")
    for s in strings:
        if s is not None and s != "":
            blocks.append(s.strip())
    return blocks

def block_to_block_type(block:str):
    if re.match(HEADER_REGEX, block) is not None:
        return BlockType.HEADING
    elif re.match(CODE_REGEX, block) is not None:
        return BlockType.CODE
    elif re.match(UNORDERED_LIST_REGEX, block) is not None:
        return BlockType.UNORDERED_LIST
    elif re.match(ORDERED_LIST_REGEX, block) is not None:
        line_num = 1
        lines = block.strip().splitlines()
        #print(lines)
        for s in lines:
            if s.startswith(f"{line_num}. "):
                line_num += 1
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    elif re.match(QUOTED_REGEX, block) is not None:
        return BlockType.QUOTE
    else:
        return BlockType.PARAGRAPH
    
