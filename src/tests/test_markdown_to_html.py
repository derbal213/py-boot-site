import unittest
from functions.markdown_to_html import markdown_to_html, block_to_block_node
from leafnode import LeafNode
from parentnode import ParentNode

class TestMarkdownToHTML(unittest.TestCase):
    def test_header_node(self):
        markdown = "### This is a header"
        node = block_to_block_node(markdown)
        expected = [LeafNode("h3", "This is a header")]
        self.assertListEqual(expected, node)
        self.assertEqual("<h3>This is a header</h3>", node[0].to_html())

    def test_code_node(self):
        markdown = "```This is a code node\nOn two lines```"
        node = block_to_block_node(markdown)
        expected = [LeafNode("code", "This is a code node\nOn two lines")]
        self.assertListEqual(expected, node)
        self.assertEqual("<code>This is a code node\nOn two lines</code>", node[0].to_html())

    def test_quote_node(self):
        markdown = ">This is a quote\n>Across multiple lines"
        node = block_to_block_node(markdown)
        expected = [ParentNode("blockquote", [LeafNode(None, "This is a quote\nAcross multiple lines")])]
        self.assertListEqual(expected, node)
        self.assertEqual("<blockquote>This is a quote\nAcross multiple lines</blockquote>", node[0].to_html())