from htmlnode import HTMLNode
from typing import Optional
from typeguard import typechecked

@typechecked
class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str], value: Optional[str], props: Optional[dict[str, str]] = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf node has no value")

        if self.tag is None:
            return self.value

        prop_string: str | None = self.props_to_html()
        prop_string = "" if prop_string is None else f" {prop_string}"
        if self.value == "":
            return f'<{self.tag}{prop_string} />'
        else:
            return f'<{self.tag}{prop_string}>{self.value}</{self.tag}>'