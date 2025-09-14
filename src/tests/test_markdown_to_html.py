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
        expected_html = "<h3>This is a header</h3>"
        self.assertEqual(expected_html, node[0].to_html())

        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())


    def test_code_node(self):
        markdown = "```This is a code node\nOn two lines```"
        node = block_to_block_node(markdown)
        expected = [LeafNode("code", "This is a code node\nOn two lines")]
        self.assertListEqual(expected, node)
        expected_html = "<code>This is a code node\nOn two lines</code>"
        self.assertEqual(expected_html, node[0].to_html())

        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())


    def test_quote_node(self):
        markdown = ">This is a quote\n>Across multiple lines"
        node = block_to_block_node(markdown)
        expected = [ParentNode("blockquote", [LeafNode(None, "This is a quote\nAcross multiple lines")])]
        self.assertListEqual(expected, node)
        expected_html = "<blockquote>This is a quote\nAcross multiple lines</blockquote>"
        self.assertEqual(expected_html, node[0].to_html())

        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())

    def test_quote_node_with_decor(self):
        markdown = ">This is a quote\n>Across **multiple** _lines_ and decor"
        node = block_to_block_node(markdown)
        expected = [ParentNode("blockquote", [
            LeafNode(None, "This is a quote\nAcross "),
            LeafNode("b", "multiple"),
            LeafNode(None, " "),
            LeafNode("i", "lines"),
            LeafNode(None, " and decor")
            ])]
        self.assertListEqual(expected, node)
        expected_html = "<blockquote>This is a quote\nAcross <b>multiple</b> <i>lines</i> and decor</blockquote>"
        self.assertEqual(expected_html, node[0].to_html())

        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())

    def test_quote_node_with_link_and_img(self):
        markdown = ">This is a quote\n>Across multiple lines, a [link](example.com) and an ![image](https://i.imgur.com/zjjcJKZ.png) inline"
        node = block_to_block_node(markdown)
        expected = [ParentNode("blockquote", [
            LeafNode(None, "This is a quote\nAcross multiple lines, a "),
            LeafNode("a", "link", {"href":"example.com"}),
            LeafNode(None, " and an "),
            LeafNode("img", "", {"src": "https://i.imgur.com/zjjcJKZ.png", "alt": "image"}),
            LeafNode(None, " inline")
            ])]
        self.assertListEqual(expected, node)
        expected_html = '<blockquote>This is a quote\nAcross multiple lines, a <a href="example.com">link</a> and an <img src="https://i.imgur.com/zjjcJKZ.png" alt="image" /> inline</blockquote>'
        self.assertEqual(expected_html, node[0].to_html())

        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())
