from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf node has no value")
        
        if self.tag is None:
            return self.value
        
        prop_string: str | None = self.props_to_html()
        if prop_string is None:
            prop_string = ""
        else:
            prop_string = " " + prop_string

        if self.value == "":
            return f'<{self.tag}{prop_string} />'
        else:
            return f'<{self.tag}{prop_string}>{self.value}</{self.tag}>'