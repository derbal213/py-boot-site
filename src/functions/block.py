from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(text):
    blocks = []
    strings = text.split("\n\n")
    for s in strings:
        if s is not None and s != "":
            blocks.append(s.strip())
    return blocks

def block_to_block_type(block:str):
    start_chars = block.split(" ", 1)
    print(start_chars)