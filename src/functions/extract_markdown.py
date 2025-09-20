import re
from src.regex_patterns import *

def extract_markdown_images(text: str) -> list[str]:
    images = re.findall(IMAGE_PATTERN, text)
    return images

def extract_markdown_links(text: str) -> list[str]:
    links = re.findall(LINK_PATTERN, text)
    return links

def extract_title(markdown: str) -> str:
    header = re.search(TITLE_PATTERN, markdown, flags=re.RegexFlag.MULTILINE)
    if header is None:
        raise Exception("Markdown does not contain a Title header (example: # Some Title)")
    
    return header.group(1)