import unittest
from functions.text_to_text_nodes import text_to_text_node
from textnode import TextNode, TextType
from parentnode import ParentNode
from functions.text_to_html import text_nodes_to_leaf_nodes

class TestTextToTextNode(unittest.TestCase):
    def test_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = text_to_text_node(text)
        self.assertListEqual(expected, actual)

    def test_to_html(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = text_to_text_node(text)
        self.assertListEqual(expected, actual)

        leaf_nodes = text_nodes_to_leaf_nodes(actual)
        parent = ParentNode("p", leaf_nodes)
        html = parent.to_html()
        expected_html = '<p>This is <b>text</b> with an <i>italic</i> word and a <code>code block</code> and an <img src="https://i.imgur.com/fJRm4Vk.jpeg" alt="obi wan image" /> and a <a href="https://boot.dev">link</a></p>'

        self.assertEqual(expected_html, html)

    def test_text_no_syntax(self):
        text = "This is text without syntax"
        expected = [
            TextNode("This is text without syntax", TextType.PLAIN)
        ]
        actual = text_to_text_node(text)
        self.assertListEqual(expected, actual)