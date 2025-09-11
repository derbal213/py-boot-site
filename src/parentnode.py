from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Must include a tag on a parent node")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("Must include children on a parent node")
        
        if self.props is None:
            str = f'<{self.tag}>'
        else:
            str = f'<{self.tag} {self.props_to_html()}>'

        for child in self.children:
            str = str + child.to_html()

        str = f'{str}</{self.tag}>'
        return str