import re
import os
from src.functions.block import block_to_block_type, markdown_to_blocks, BlockType
from src.leafnode import LeafNode
from src.parentnode import ParentNode
from src.functions.text_to_text_nodes import text_to_text_nodes
from src.functions.text_to_html import text_nodes_to_leaf_nodes
from src.regex_patterns import *
from src.functions.extract_markdown import extract_title
from src.htmlnode import HTMLNode
from src.textnode import TextNode
from src.functions.file_handler import read_file, write_file, check_directory

# Takes a markdown text, converts it to text blocks
# Then for each block converts that block to HTMLNode(s)
# Finally wraps it in a parent div tag
def markdown_to_html(markdown: str) -> ParentNode:
    md_blocks: list[str] = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []
    for block in md_blocks:
        children.extend(block_to_block_node(block))

    div = ParentNode("div", children)
    return div

# Converts a text block to an HTMLNode
# The block type determines whether it is a ParentNode or a LeafNode
def block_to_block_node(block: str) -> list[HTMLNode]:
    block_type: BlockType = block_to_block_type(block)
    match block_type:
        case BlockType.CODE:
            return [LeafNode("code", block[3:-3])]
        case BlockType.HEADING:
            hashes: str = block.split(" ", 1)[0]
            count_hash: int = len(hashes)
            return [text_to_parent(block[count_hash + 1:], f"h{count_hash}", block_type)]
        case BlockType.QUOTE:
            modified_quote: str = re.sub(QUOTE_REMOVE_PATTERN, "", block).strip()
            return [text_to_parent(modified_quote, "blockquote")]
        case BlockType.UNORDERED_LIST:
            modified_unordered: str = re.sub(UNORDERED_LIST_REMOVE_PATTERN, "", block).strip()
            return [text_to_parent(modified_unordered, "ul", block_type)]
        case BlockType.ORDERED_LIST:
            modified_ordered: str = re.sub(ORDERED_LIST_REMOVE_PATTERN, "", block).strip()
            return [text_to_parent(modified_ordered, "ol", block_type)]
        case _:
            return [text_to_parent(block, "p", block_type)]
        
# Create a ParentNode with a given parent tag for when a text block
# is likely to have nested syntax (such as paragraphs)
def text_to_parent(text: str, parent_tag: str, block_type: BlockType = BlockType.PARAGRAPH) -> ParentNode:
    nodes: list[HTMLNode] = []
    if block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
        list_items: list[str] = text.splitlines() #For lists, we already know it's a valid list so each line is am HTML node
        for item in list_items:
            item_nodes: list[TextNode] = text_to_text_nodes(item)
            leaf_nodes: list[HTMLNode] = text_nodes_to_leaf_nodes(item_nodes) # This ensures that any decoration within the list item is captured
            nodes.append(ParentNode("li", leaf_nodes))
    else:
        text_nodes: list[TextNode] = text_to_text_nodes(text)
        nodes.extend(text_nodes_to_leaf_nodes(text_nodes, block_type))
    return ParentNode(parent_tag, nodes)

# Generate HTML pages from markdown files located in a content directory
# Runs recursively for all subdirectories
def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str = "/") -> None:
    items: list[str] = os.listdir(dir_path_content)
    for i in items:
        path: str = os.path.join(dir_path_content, i)
        ext: str = os.path.splitext(i)[1]
        if os.path.isfile(path):
            if ext == ".md":
                generate_page(path, template_path, os.path.join(dest_dir_path, i.replace(ext, ".html")), base_path)
            else:
                print(f"Skipping file without .md extension: {path}")
        else:
            # Directory
            new_dest: str = os.path.join(dest_dir_path, i)
            generate_pages_recursive(path, template_path, new_dest, base_path)


# Generate an HTML file from a markdown file
def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str = "/") -> None:
    print(f"-> Generating page from {from_path}\n---> TO {dest_path}\n---> USING {template_path}")
    src_content: str = read_file(from_path)
    template_content: str = read_file(template_path)
    title: str = extract_title(src_content)
    html: str = markdown_to_html(src_content).to_html()

    final_content: str = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)
    final_content = final_content.replace('href="/', f'href="{base_path}')
    final_content = final_content.replace('src="/', f'src="{base_path}')
    
    check_directory(dest_path)
    write_file(dest_path, final_content)