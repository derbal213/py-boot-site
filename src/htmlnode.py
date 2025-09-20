class HTMLNode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("Not yet implemented")
    
    def props_to_html(self) -> str | None:
        if self.props is not None:
            str = ""
            for key in self.props:
                value = self.props[key]
                str = f'{str} {key}="{value}"'
            str = str.strip()
            return str
        else:
            return None
    
    def is_blank(self) -> bool:
        if self.tag is not None:
            return False
        if self.value is not None and self.value != "":
            return False
        if self.props is not None and len(self.props) > 0:
            return False
        if self.children is not None and len(self.children) > 0:
            return False
        return True

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
    
    def __eq__(self, value) -> bool:
        if self.tag != value.tag:
            return False
        if self.value != value.value:
            return False
        if self.children != value.children:
            return False
        if self.props != value.props:
            return False
        return True