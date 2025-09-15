import re
import os
from functions.block import block_to_block_type, markdown_to_blocks, BlockType
from leafnode import LeafNode
from parentnode import ParentNode
from functions.text_to_text_nodes import text_to_text_nodes
from functions.text_to_html import text_nodes_to_leaf_nodes
from regex import *
from functions.extract_markdown import extract_title

# Takes a markdown text, converts it to text blocks
# Then for each block converts that block to HTMLNode(s)
# Finally wraps it in a parent div tag
def markdown_to_html(markdown):
    md_blocks = markdown_to_blocks(markdown)
    children = []
    for block in md_blocks:
        nodes = block_to_block_node(block)
        children.extend(nodes)

    div = ParentNode("div", children)
    return div

# Converts a text block to an HTMLNode
# The block type determines whether it is a ParentNode or a LeafNode
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
            modified_text = re.sub(QUOTE_REMOVE_PATTERN, "", block).strip()
            return [text_to_parent(modified_text, "blockquote")]
        case BlockType.UNORDERED_LIST:
            modified_text = re.sub(UNORDERED_LIST_REMOVE_PATTERN, "", block).strip()
            return [text_to_parent(modified_text, "ul", block_type)]
        case BlockType.ORDERED_LIST:
            modified_text = re.sub(ORDERED_LIST_REMOVE_PATTERN, "", block).strip()
            return [text_to_parent(modified_text, "ol", block_type)]
        case _:
            return [text_to_parent(block, "p", block_type)]
        
# Create a ParentNode with a given parent tag for when a text block
# is likely to have nested syntax (such as paragraphs)
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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    src_content = read_file(from_path)
    template_content = read_file(template_path)
    title = "Converted Markdown"
    try:
        title = extract_title(src_content)
    except Exception as e:
        print(f"Error when extracting title. Using default title. Error: {e}")

    html = markdown_to_html(src_content).to_html()
    final_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)
    check_directory(dest_path)
    write_file(dest_path, final_content)


def read_file(path):
    with open(path, 'r') as src_file:
        if src_file is None:
            raise Exception(f"File could not be read at {path}")
        src_contents = src_file.read()
        #os.close(src_file)
        return src_contents
    
def write_file(path, contents):
    with open(path, 'w') as file:
        file.write(contents)

def check_directory(path):
    dir = os.path.dirname(path)
    os.makedirs(dir, 0o777, True)