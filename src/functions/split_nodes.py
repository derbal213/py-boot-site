import re
from src.textnode import TextType, TextNode
from src.functions.extract_markdown import extract_markdown_images, extract_markdown_links
from src.regex_patterns import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            parts: list[str] = node.text.split(delimiter)
            new_parts: list[TextNode] = []
            for i in range(len(parts)):
                if i % 2 == 0:
                    new_parts.append(TextNode(parts[i], TextType.PLAIN))
                else:
                    new_parts.append(TextNode(parts[i], text_type))
            new_nodes.extend(new_parts)
    return new_nodes


def split_nodes_image_and_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            images: list[str] = extract_markdown_images(node.text)
            links: list[str] = extract_markdown_links(node.text)
            # Do an initial check to see if there are any links or images at all
            # If none, add the node unchanged. If there are, then parse it out correctly
            if len(images) == 0 and len(links) == 0:
                new_nodes.append(node)
            else:
                parts: list[str] = split_markdown_on_imgs_links(node.text)
                for p in parts:
                    if re.match(IMAGE_PATTERN, p):
                        images = extract_markdown_images(p)
                        for img in images:
                            img_node: TextNode = TextNode(img[0], TextType.IMAGE, img[1])
                            new_nodes.append(img_node)
                    elif re.match(LINK_PATTERN, p):
                        links = extract_markdown_links(p)
                        for link in links:
                            link_node: TextNode = TextNode(link[0], TextType.LINK, link[1])
                            new_nodes.append(link_node)
                    else:
                        plain_node = TextNode(p, TextType.PLAIN)
                        new_nodes.append(plain_node)
    return new_nodes

# Split markdown on images and links
def split_markdown_on_imgs_links(text: str) -> list[str]:
    parts: list[str] = []
    last: int = 0
    for match in re.finditer(IMAGE_OR_LINK_PATTERN, text):
        # Add text before the match
        if match.start() > last:
            parts.append(text[last:match.start()])
        parts.append(match.group(0))
        last = match.end()
    
    # Add any remaining text after the last match
    if last < len(text):
        parts.append(text[last:])
    
    return parts