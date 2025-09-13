from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from functions.extract_markdown import extract_markdown_images, extract_markdown_links
from functions.text_to_text_nodes import text_to_text_node

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(text_node)
    
    props = {"href":"boot.dev", "target":"_blank"}
    props2 = {"href":"boot.dev"}
    child = HTMLNode("a", "This is a child", None, props2)
    html_node = HTMLNode("p", "This is a paragraph", child, props)
    #print(html_node)

    node = LeafNode("i", "Hello, world!")
    #print(node.to_html())

    parentNode = ParentNode("p", [node])
    #print(parentNode.to_html())

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    #print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    #print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

    text= "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    text_to_text_node(text)
    
if __name__ == "__main__":
    main()