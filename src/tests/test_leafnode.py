import unittest
from leafnode import LeafNode
from typeguard import TypeCheckError

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        props = {"href":"boot.dev", "target":"_blank"}
        node = LeafNode("a", "Hello, world!", props)
        expected = '<a href="boot.dev" target="_blank">Hello, world!</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
        
    def test_invalid_tag_type(self):
        with self.assertRaises(TypeCheckError):
            LeafNode(123, "Hello, world!")  # tag should be str or None

    def test_invalid_content_type(self):
        with self.assertRaises(TypeCheckError):
            LeafNode("p", 456)  # content should be str

    def test_invalid_props_type(self):
        with self.assertRaises(TypeCheckError):
            LeafNode("a", "Hello, world!", ["not", "a", "dict"])  # props should be dict

    def test_invalid_tag_object(self):
        with self.assertRaises(TypeCheckError):
            LeafNode(object(), "Hello, world!")  # tag should be str or None

    def test_invalid_props_none(self):
        # props can be None, so this should not raise
        try:
            LeafNode("a", "Hello, world!", None)
        except Exception as e:
            self.fail(f"LeafNode raised {type(e)} unexpectedly with props=None")