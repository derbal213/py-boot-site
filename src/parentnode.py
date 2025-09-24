from htmlnode import HTMLNode
from typing import Optional

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: Optional[dict[str, str]] = None):
        if tag is None:
            raise ValueError("Must include a tag on a parent node")
        if children is None or not children:
            raise ValueError("Must include children on a parent node")

        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        html: str = f'<{self.tag} {self.props_to_html()}>' if self.props is not None else f'<{self.tag}>'

        if self.children:
            for child in self.children:
                html = html + child.to_html()

        return f'{html}</{self.tag}>'