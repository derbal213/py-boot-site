import re
from functions.block import block_to_block_type, markdown_to_blocks, BlockType
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, TextTypeSyntax
from functions.text_to_text_nodes import text_to_text_nodes
from functions.text_to_html import text_node_to_html_node, text_nodes_to_leaf_nodes

QUOTE_REMOVE_REGEX = r'(?m)^>'
UNORDERED_LIST_REMOVE_REGEX = r'(?m)^- '
ORDERED_LIST_REMOVE_REGEX = r'(?m)^\d\. '

def markdown_to_html(markdown):
    md_blocks = markdown_to_blocks(markdown)
    children = []
    for block in md_blocks:
        nodes = block_to_block_node(block)
        children.extend(nodes)

    div = ParentNode("div", children)
    return div

def block_to_block_node(block: str):
    block_type = block_to_block_type(block)
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
            return [text_to_parent(modified_text, "blockquote")]
        case BlockType.UNORDERED_LIST:
            modified_text = re.sub(UNORDERED_LIST_REMOVE_REGEX, "", block)
            return [text_to_parent(modified_text, "ul", block_type)]
        case BlockType.ORDERED_LIST:
            modified_text = re.sub(ORDERED_LIST_REMOVE_REGEX, "", block)
            return [text_to_parent(modified_text, "ol", block_type)]
        case _:
            return [text_to_parent(block, "p", block_type)]
        

def text_to_parent(text, parent_tag, block_type: BlockType = None):
    text_nodes = []
    nodes = []
    if block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
        list_items = text.splitlines() #For lists, we already know it's a valid list so split out the lines into their own TextNodes
        for item in list_items:
            item_nodes = text_to_text_nodes(item)
            leaf_nodes = text_nodes_to_leaf_nodes(item_nodes)
            nodes.append(ParentNode("li", leaf_nodes))
    else:
        text_nodes = text_to_text_nodes(text)
        nodes = text_nodes_to_leaf_nodes(text_nodes, block_type)
    return ParentNode(parent_tag, nodes)

#def leaf_to_parent(leaf_node: LeafNode):
