from textnode import TextType, TextNode, TextTypeSyntax
from functions.extract_markdown import extract_markdown_images, extract_markdown_links, IMAGE_PATTERN, LINK_PATTERN
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            #print(len(parts))
            new_parts = []
            for i in range(len(parts)):
                if i % 2 == 0:
                    new_parts.append(TextNode(parts[i], TextType.PLAIN))
                else:
                    new_parts.append(TextNode(parts[i], text_type))
            new_nodes.extend(new_parts)
    return new_nodes

def split_nested_delimiter(old_nodes: list[TextNode], outer_text_type = TextType.PLAIN):
    new_nodes = []
    for node in old_nodes:
        print(f"-----> Current Node: {node}")
        delimiter = get_outer_delimiter(node)
        print(f"----> Delimiter: {delimiter}")
        if delimiter is None:
            new_nodes.append(node)
        else:      
            if delimiter is None:
                new_nodes.append(node)
            else:
                text_type = TextType.PLAIN
                match delimiter:
                    case TextTypeSyntax.BOLD:
                        text_type = TextType.BOLD
                    case TextTypeSyntax.ITALIC:
                        text_type = TextType.ITALIC
                    case TextTypeSyntax.CODE:
                        text_type = TextType.CODE
                parts = node.text.split(delimiter)
                #print(f"-----> Text type: {text_type}")
                #print(f"-----> Parts: {parts}")
                new_parts = []
                for i in range(len(parts)):
                    if i % 2 == 0: #Represents a block before/after a split element
                        new_parts.append(TextNode(parts[i], outer_text_type))
                    else: #Represent an element within the delimiter
                        text_node = TextNode(parts[i], text_type)
                        nested_nodes = split_nested_delimiter([text_node], text_type)
                        new_parts.append(nested_nodes)
                new_nodes.extend(new_parts)
    return new_nodes

def get_outer_delimiter(node: TextNode):
    first_index = None
    first_delim = None

    for delim in TextTypeSyntax.ALL_OPTIONS:
        index = node.text.find(delim)
        if index != -1:
            if first_index is None or index < first_index:
                first_index = index
                first_delim = delim
    
    return first_delim

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
                #print(parts)
                #parts = [p for p in parts if p and not p.isspace()]
                for p in parts:
                    #print(f"----->Part: {p}")
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

def split_markdown(text):
    pattern = r'!\[[^\]]*\]\([^)]*\)|(?<!!)\[[^\]]*\]\([^)]*\)'
    
    parts = []
    last = 0
    for match in re.finditer(pattern, text):
        # Add text before the match
        if match.start() > last:
            parts.append(text[last:match.start()])
        parts.append(match.group(0))
        last = match.end()
    
    # Add any remaining text after the last match
    if last < len(text):
        parts.append(text[last:])
    
    return parts