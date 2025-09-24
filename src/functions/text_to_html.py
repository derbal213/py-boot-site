from textnode import TextNode, TextType
from leafnode import LeafNode
from functions.block import BlockType
from htmlnode import HTMLNode
from typing import Optional

# Convert a TextNode to a LeafNode
def text_node_to_html_node(text_node: Optional[TextNode], block_type: BlockType = BlockType.PARAGRAPH) -> Optional[HTMLNode]:
    if text_node is None:
        return None

    # Tag can (and sometimes should) be None and that case is handled elsewhere
    tag: Optional[str] = get_tag(text_node.text_type, block_type)
    text = "" if text_node.text_type == TextType.IMAGE else text_node.text
    return LeafNode(tag, text, get_props(text_node))
        
# Get the properties of a text node for links and images
def get_props(text_node: TextNode) -> Optional[dict]:
    match text_node.text_type:
        case TextType.LINK:
            return {"href": text_node.url}
        case TextType.IMAGE:
            props: dict[str, str] = {}
            if text_node.url is not None:
                props["src"] = text_node.url
            if text_node.text is not None:
                props["alt"] = text_node.text
            return props or None
        case _:
            return None

# Get the tag for a given text type
def get_tag(text_type: TextType, block_type: BlockType = BlockType.PARAGRAPH) -> str | None:
        match text_type:
            case TextType.PLAIN:
                if block_type in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
                    return "li"
                else:
                    return None
            case TextType.BOLD:
                return "b"
            case TextType.ITALIC:
                return "i"
            case TextType.CODE:
                return "code"
            case TextType.LINK:
                return "a"
            case TextType.IMAGE:
                return "img"
            case _:
                raise ValueError("Text type does not match an HTML tag")

# Convert TextNodes to LeafNodes    
def text_nodes_to_leaf_nodes(text_nodes: list[TextNode], block_type: BlockType = BlockType.PARAGRAPH) -> Optional[list[HTMLNode]]:
    if text_nodes is None:
        return None
    
    leaf_nodes: list[HTMLNode] = []
    for n in text_nodes:
        html_node: HTMLNode | None = text_node_to_html_node(n, block_type)
        # .is_blank returns false for nodes that have no text but do have attributes (like img)
        if html_node and not html_node.is_blank():
            leaf_nodes.append(html_node)
    return leaf_nodes