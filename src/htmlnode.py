class HTMLNode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("Not yet implemented")
    
    def props_to_html(self) -> str | None:
        if self.props is None:
            return None
        if len(self.props) == 0:
            return None
        
        props_str = ""
        for key in self.props:
            value = self.props[key]
            props_str = f'{props_str} {key}="{value}"'
        return props_str.strip()
    
    def is_blank(self) -> bool:
        if self.tag is not None:
            return False
        elif self.value is not None and self.value != "":
            return False
        elif self.props is not None and len(self.props) > 0:
            return False
        elif self.children is not None and len(self.children) > 0:
            return False
        else: 
            return True

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
    
    def __eq__(self, value) -> bool:
        if not isinstance(value, HTMLNode):
            return NotImplemented
        elif self.tag != value.tag:
            return False
        elif self.value != value.value:
            return False
        elif self.children != value.children:
            return False
        elif self.props != value.props:
            return False
        else:
            return True