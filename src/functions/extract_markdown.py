import re

def extract_markdown_images(text):
    pattern = r'!\[([^\]]*)\]\(([^)]*)\)'
    images = re.findall(pattern, text)
    return images

def extract_markdown_links(text):
    pattern = r'(?<!!)\[([^\]]*)\]\(([^)]*)\)'
    links = re.findall(pattern, text)
    return links