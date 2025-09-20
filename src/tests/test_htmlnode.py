import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_equal_empty(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_equal_no_children(self):
        props = {"href":"boot.dev", "target":"_blank"}
        node = HTMLNode("p", "This is a paragraph", None, props)
        node2 = HTMLNode("p", "This is a paragraph", None, props)
        self.assertEqual(node, node2)

    def test_equal_full(self):
        props = {"href":"boot.dev", "target":"_blank"}
        props2 = {"href":"boot.dev"}
        child = HTMLNode("a", "This is a child", None, props2)
        node = HTMLNode("p", "This is a paragraph", child, props)
        node2 = HTMLNode("p", "This is a paragraph", child, props)
        self.assertEqual(node, node2)

    def test_repr(self):
        props = {"href":"boot.dev", "target":"_blank"}
        props2 = {"href":"boot.dev"}
        child = HTMLNode("a", "This is a child", None, props2)
        node = HTMLNode("p", "This is a paragraph", child, props)
        expected = 'HTMLNode(p, This is a paragraph, HTMLNode(a, This is a child, None, href="boot.dev"), href="boot.dev" target="_blank")'
        self.assertEqual(str(node), expected)

    def test_props_to_html(self):
        props = {"href":"boot.dev", "target":"_blank"}
        node = HTMLNode("p", "This is a paragraph", None, props)
        result = node.props_to_html()
        expected = 'href="boot.dev" target="_blank"'
        self.assertEqual(result, expected)