from src.functions.split_nodes import split_nodes_on_images_and_links, split_nodes_on_delimiter
from src.textnode import TextNode, TextType, TextTypeSyntax

def text_to_text_nodes(text:str) -> list[TextNode]:
    base_node: TextNode = TextNode(text, TextType.PLAIN)

    new_nodes: list[TextNode] = split_nodes_on_delimiter([base_node], TextTypeSyntax.BOLD, TextType.BOLD)
    new_nodes = split_nodes_on_delimiter(new_nodes, TextTypeSyntax.ITALIC, TextType.ITALIC)
    new_nodes = split_nodes_on_delimiter(new_nodes, TextTypeSyntax.CODE, TextType.CODE)
    new_nodes = split_nodes_on_images_and_links(new_nodes)
    
    return new_nodes