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
    ALL_OPTIONS = [BOLD, ITALIC, CODE]

class TextNode():
    def __init__(self, text, text_type, url=None, text_types=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        if text_types is None:
            self.text_types = [text_type]
        else: 
            self.text_types = text_types

    def __eq__(self, value):
        if self.text != value.text:
            return False
        if self.text_type != value.text_type:
            return False
        if self.url != value.url:
            return False
        return True
    
    def __repr__(self):
        text_types = f"[{",".join([t.value for t in self.text_types])}]"
        return f"TextNode({self.text}, {self.text_type.value}, {self.url}, {text_types})"