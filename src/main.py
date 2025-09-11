from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)
    
    props = {"href":"boot.dev", "target":"_blank"}
    props2 = {"href":"boot.dev"}
    child = HTMLNode("a", "This is a child", None, props2)
    html_node = HTMLNode("p", "This is a paragraph", child, props)
    print(html_node)

if __name__ == "__main__":
    main()