from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            return ValueError("Leaf node has no value")
        
        if self.tag is None:
            return self.value
        
        prop_string = self.props_to_html()
        if prop_string is None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag} {prop_string}>{self.value}</{self.tag}>'