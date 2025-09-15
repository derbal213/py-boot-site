import re
from regex import *

def extract_markdown_images(text):
    images = re.findall(IMAGE_PATTERN, text)
    return images

def extract_markdown_links(text):
    links = re.findall(LINK_PATTERN, text)
    return links

