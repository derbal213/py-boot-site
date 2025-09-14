from functions.split_nodes import split_nodes_image_and_links, split_nodes_delimiter
from textnode import TextNode, TextType, TextTypeSyntax

def text_to_text_nodes(text:str):
    base_node = TextNode(text, TextType.PLAIN)

    new_nodes = split_nodes_delimiter([base_node], TextTypeSyntax.BOLD, TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, TextTypeSyntax.ITALIC, TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, TextTypeSyntax.CODE, TextType.CODE)
    new_nodes = split_nodes_image_and_links(new_nodes)
    
    return new_nodes

""" def text_to_text_node_helper(new_nodes: list[TextNode], text_type):
    added_nodes = []
    for node in new_nodes:
       match text_type:
           case TextType.BOLD:
               added_nodes.extend(split_nodes_delimiter()) """