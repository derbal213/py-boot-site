import re
import logging
from regex_patterns import IMAGE_PATTERN, LINK_PATTERN, TITLE_PATTERN

def extract_markdown_images(text: str) -> list[str]:
    return re.findall(IMAGE_PATTERN, text)

def extract_markdown_links(text: str) -> list[str]:
    return re.findall(LINK_PATTERN, text)

def extract_title(markdown: str) -> str:
    header = re.search(TITLE_PATTERN, markdown, flags=re.RegexFlag.MULTILINE)
    if header is None or header[1] is None:
        logging.warning("No top level header found in markdown. Using default title.")
        return "Default Title"
    
    return header[1]

def main():
    pass

if __name__ == "__main__":
    main()