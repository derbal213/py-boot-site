from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextTypeSyntax:
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"
    LINK = "["
    IMAGE = "!["
    LINK_IMAGE_END = "]"
    ALL_OPTIONS = [BOLD, ITALIC, CODE, LINK, IMAGE]

class TextNode():
    def __init__(self, text: str, text_type, url=None, child_nodes = None):
        self.text = text
        self.text_type = text_type
        self.url = url
        self.children = child_nodes

    def __eq__(self, value):
        if self.text != value.text:
            return False
        if self.text_type != value.text_type:
            return False
        if self.url != value.url:
            return False
        if self.children != value.children:
            return False
        return True
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url}, {self.children})"