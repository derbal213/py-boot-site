from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: None | dict[str, str] = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Must include a tag on a parent node")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("Must include children on a parent node")
        
        html: str = ""
        if self.props is None:
            html = f'<{self.tag}>'
        else:
            html = f'<{self.tag} {self.props_to_html()}>'

        for child in self.children:
            html = html + child.to_html()

        html = f'{html}</{self.tag}>'
        return html