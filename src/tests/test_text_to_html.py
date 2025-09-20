import unittest
from textnode import TextNode, TextType
from functions.text_to_html import text_node_to_html_node

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "boot.dev")
        html_node = text_node_to_html_node(node)
        expected = '<a href="boot.dev">This is a link node</a>'
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.to_html(), expected)

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        expected = '<b>This is a bold node</b>'
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.to_html(), expected)

    def test_bold_with_link(self):
        node = TextNode("This is a bold node", TextType.BOLD, "boot.dev")
        html_node = text_node_to_html_node(node)
        expected = '<b>This is a bold node</b>'
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.to_html(), expected)

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        expected = '<i>This is an italic node</i>'
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
        self.assertEqual(html_node.to_html(), expected)

    def test_italic_with_link(self):
        node = TextNode("This is an italic node", TextType.ITALIC, "boot.dev")
        html_node = text_node_to_html_node(node)
        expected = '<i>This is an italic node</i>'
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
        self.assertEqual(html_node.to_html(), expected)

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        expected = '<code>This is a code node</code>'
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.to_html(), expected)

    def test_code_with_link(self):
        node = TextNode("This is a code node", TextType.CODE, "boot.dev")
        html_node = text_node_to_html_node(node)
        expected = '<code>This is a code node</code>'
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.to_html(), expected)

    def test_img(self):
        node = TextNode("This is an img node", TextType.IMAGE, "boot.dev")
        html_node = text_node_to_html_node(node)
        expected = '<img src="boot.dev" alt="This is an img node" />'
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), expected)

    def test_img_no_text(self):
        node = TextNode(None, TextType.IMAGE, "boot.dev")
        html_node = text_node_to_html_node(node)
        expected = '<img src="boot.dev" />'
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), expected)

    def test_img_no_url(self):
        node = TextNode("This is an img node", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        expected = '<img alt="This is an img node" />'
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), expected)

    def test_img_just_tag(self):
        node = TextNode(None, TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        expected = '<img />'
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), expected)