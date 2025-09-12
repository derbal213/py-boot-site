import unittest
from functions.split_nodes_delimiter import split_nodes_delimiter, split_nested_delimiter
from functions.text_to_html import text_node_to_html_node, text_nodes_to_leaf_nodes
from textnode import TextNode, TextType, TextTypeSyntax
from parentnode import ParentNode

class TestSplitNode(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        expected = TextNode("code block", TextType.CODE)
        self.assertEqual(expected, new_nodes[1])

    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextTypeSyntax.BOLD, TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        expected = TextNode("bold", TextType.BOLD)
        self.assertEqual(expected, new_nodes[1])

    def test_italic(self):
        node = TextNode(f"This is text with an _italic_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextTypeSyntax.ITALIC, TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        expected = TextNode("italic", TextType.ITALIC)
        self.assertEqual(expected, new_nodes[1])

    def test_convert_to_HTML(self):
        node = TextNode(f"This is text with an _italic_ word", TextType.PLAIN)
        node2 = TextNode("This is text with a **bold** word", TextType.PLAIN)
        node3 = TextNode("This is text with a `code block` word", TextType.PLAIN)
        nodes = [node, node2, node3]
        expected_vals = [
            "<p>This is text with an <i>italic</i> word</p>",
            "<p>This is text with a <b>bold</b> word</p>",
            "<p>This is text with a <code>code block</code> word</p>"
        ]
        syntaxes = [TextTypeSyntax.ITALIC, TextTypeSyntax.BOLD, TextTypeSyntax.CODE]
        text_types = [TextType.ITALIC, TextType.BOLD, TextType.CODE]

        for i in range(0, len(nodes) - 1):
            new_nodes = split_nodes_delimiter([nodes[i]], syntaxes[i], text_types[i])
            leaf_nodes = text_nodes_to_leaf_nodes(new_nodes)
            parent_node = ParentNode("p", leaf_nodes)
            expected = expected_vals[i]
            #print(expected)
            self.assertEqual(expected, parent_node.to_html())
    
    """ def test_nested(self):
        node = TextNode(f"This is text with an _italic and **bold**_ word", TextType.PLAIN)
        new_nodes = split_nested_delimiter([node])
        print(new_nodes)
        self.assertEqual(5, len(new_nodes))

        leaf_nodes = text_nodes_to_leaf_nodes(new_nodes)
        parent = ParentNode("p", leaf_nodes)
        expected = "<p>This is text with an <i>italic and <b>bold</b></i> word</p>"
        self.assertEqual(expected, parent.to_html()) """
