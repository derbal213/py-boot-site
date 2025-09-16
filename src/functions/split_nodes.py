from textnode import TextType, TextNode
from functions.extract_markdown import extract_markdown_images, extract_markdown_links
import re
from regex import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            new_parts = []
            for i in range(len(parts)):
                if i % 2 == 0:
                    new_parts.append(TextNode(parts[i], TextType.PLAIN))
                else:
                    new_parts.append(TextNode(parts[i], text_type))
            new_nodes.extend(new_parts)
    return new_nodes


def split_nodes_image_and_links(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            links = extract_markdown_links(node.text)
            if len(images) == 0 and len(links) == 0:
                new_nodes.append(node)
            else:
                parts = split_markdown(node.text)
                for p in parts:
                    if re.match(IMAGE_PATTERN, p):
                        images = extract_markdown_images(p)
                        for img in images:
                            img_node = TextNode(img[0], TextType.IMAGE, img[1])
                            new_nodes.append(img_node)
                    elif re.match(LINK_PATTERN, p):
                        links = extract_markdown_links(p)
                        for link in links:
                            link_node = TextNode(link[0], TextType.LINK, link[1])
                            new_nodes.append(link_node)
                    else:
                        plain_node = TextNode(p, TextType.PLAIN)
                        new_nodes.append(plain_node)
    return new_nodes

# Split markdown on images and links
def split_markdown(text):
    parts = []
    last = 0
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