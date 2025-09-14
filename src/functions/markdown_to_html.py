import re
from functions.block import block_to_block_type, markdown_to_blocks, BlockType
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, TextTypeSyntax
from functions.text_to_text_nodes import text_to_text_node
from functions.text_to_html import text_node_to_html_node, text_nodes_to_leaf_nodes

QUOTE_REMOVE_REGEX = r'(?m)^>'

def markdown_to_html(markdown):
    md_blocks = markdown_to_blocks(markdown)
    for block in md_blocks:
        nodes = block_to_block_node(block)

def block_to_block_node(block: str):
    block_type = block_to_block_type(block)
    text_node = None
    match block_type:
        case BlockType.CODE:
            return [LeafNode("code", block[3:-3])]
        case BlockType.HEADING:
            hashes = block.split(" ", 1)[0]
            #print(hashes)
            count_hash = len(hashes)
            html_node = LeafNode(f"h{count_hash}", block[count_hash + 1:])
            return [html_node]
        case BlockType.QUOTE:
            modified_text = re.sub(QUOTE_REMOVE_REGEX, "", block)
            text_node = text_to_text_node(modified_text)
            nodes = text_nodes_to_leaf_nodes(text_node)
            return [ParentNode("blockquote", nodes)]