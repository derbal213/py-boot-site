class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not yet implemented")
    
    def props_to_html(self):
        if self.props is not None:
            str = ""
            for key in self.props:
                value = self.props[key]
                str = f'{str} {key}="{value}"'
            str = str.strip()
            return str
        else:
            return None
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
    
    def __eq__(self, value):
        if self.tag != value.tag:
            return False
        if self.value != value.value:
            return False
        if self.children != value.children:
            return False
        if self.props != value.props:
            return False
        return True