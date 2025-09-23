import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_none(self):
        node = TextNode("This is a link node", TextType.LINK)
        node2 = TextNode("This is a link node", TextType.LINK)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is an italic node", TextType.ITALIC, "boot.dev")
        expected = 'TextNode("This is an italic node", "italic", "boot.dev")'
        result = str(node)
        self.assertEqual(result, expected)

    def test_repr_none(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        expected = 'TextNode("This is a text node", "plain", "None")'
        result = str(node)
        self.assertEqual(result, expected)

    def test_type_not_equal(self):
        node = TextNode("This is a text", TextType.PLAIN)
        node2 = TextNode("This is a text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_not_equal(self):
        node = TextNode("This is a text", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_url_not_equal(self):
        node = TextNode("This is a link", TextType.LINK, "boot.dev")
        node2 = TextNode("This is a link", TextType.LINK, "google.com")
        self.assertNotEqual(node, node2)

    def test_no_type(self):
        with self.assertRaises(TypeError):
            TextNode("This is text without a type")

if __name__ == "__main__":
    unittest.main()