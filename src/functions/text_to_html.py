from textnode import TextNode, TextType
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode

def text_node_to_html_node(text_node: TextNode):
    if text_node is None:
        return None
    
    match text_node.text_type:
        case TextType.PLAIN:
            node = LeafNode(None, text_node.text)
            return node
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            props = {}
            if text_node.url is not None:
                props["src"] = text_node.url
            if text_node.text is not None:
                props["alt"] = text_node.text
            if len(props) == 0: props = None
            return LeafNode("img", "", props)
        case _:
            raise ValueError("Text type does not match an HTML tag")
        
def text_nodes_to_leaf_nodes(text_nodes: list[TextNode]):
    if text_nodes is None:
        return None
    
    leaf_nodes = []
    for n in text_nodes:
        leaf_nodes.append(text_node_to_html_node(n))
    return leaf_nodes