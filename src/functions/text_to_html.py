from textnode import TextNode, TextType
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from functions.block import BlockType

# Convert a TextNode to a LeafNode
def text_node_to_html_node(text_node: TextNode, block_type: BlockType = None):
    if text_node is None:
        return None
    
    tag = get_tag(text_node.text_type, block_type)
    text = text_node.text
    if text_node.text_type == TextType.IMAGE:
        text = ""
    return LeafNode(tag, text, get_props(text_node))
        
# Get the properties of a text node for links and images
def get_props(text_node: TextNode):
    match text_node.text_type:
        case TextType.LINK:
            return {"href":text_node.url}
        case TextType.IMAGE:
            props = {}
            if text_node.url is not None:
                props["src"] = text_node.url
            if text_node.text is not None:
                props["alt"] = text_node.text
            if len(props) == 0: props = None
            return props
        case _:
            return None

# Get the tag for a given text type
def get_tag(text_type: TextType, block_type: BlockType = None):
        match text_type:
            case TextType.PLAIN:
                if block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
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
def text_nodes_to_leaf_nodes(text_nodes: list[TextNode], block_type: BlockType = None):
    if text_nodes is None:
        return None
    
    leaf_nodes = []
    for n in text_nodes:
        leaf_nodes.append(text_node_to_html_node(n, block_type))
    return leaf_nodes


# def text_nodes_with_children_to_html(text_nodes: list[TextNode], block_type: BlockType = None):
#     if text_nodes is None:
#         return None
    
#     nodes = []
#     for n in text_nodes:
#         if n.text == "" and len(n.children) > 0:
#             children = []
#             for child in n.children:
#                 child_html = text_nodes_with_children_to_html([child], block_type)
#                 children.extend(child_html)        
#             nodes.append(ParentNode(get_tag(n.text_type, block_type), children, get_props(n)))
#         else:
#             nodes.append(text_node_to_html_node(n, block_type))
#     return nodes