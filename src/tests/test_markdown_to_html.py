import unittest
from functions.markdown_to_html import markdown_to_html, block_to_block_node
from leafnode import LeafNode
from parentnode import ParentNode

class TestMarkdownToHTML(unittest.TestCase):
    block_md = """
This is a **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

### This is **a** _header_

```This is a code block
across two lines```

1. This is an ordered list
2. With multiple items

- This is an unordered list
- with items

>This is a quote
>That goes onto two lines
>-Michael Scott
"""

    block_extra_line_md = """
This is a **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


### This is a header


```This is a code block
across two lines```


1. This is an ordered list
2. With multiple items


- This is an unordered list
- with items


>This is a quote
>That goes onto two lines
>-Michael Scott
"""

    def test_header_node(self):
        markdown = "### This is a header"
        node = block_to_block_node(markdown)
        expected = [ParentNode("h3", [LeafNode(None, "This is a header")])]
        self.assertListEqual(expected, node)
        expected_html = "<h3>This is a header</h3>"
        self.assertEqual(expected_html, node[0].to_html())

        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())

    def test_header_stylized(self):
        markdown = "### This is **a** _header_"
        node = block_to_block_node(markdown)
        print(node)
        expected = [ParentNode("h3", [
                LeafNode(None, "This is "),
                LeafNode("b", "a"), 
                LeafNode(None, " "),
                LeafNode("i", "header")])]
        print(expected)
        self.assertListEqual(expected, node)
        expected_html = "<h3>This is <b>a</b> <i>header</i></h3>"
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

    def test_unordered_plain(self):
        markdown = "- This is an unordered list\n- With multiple entries\n- It is valid"
        node = block_to_block_node(markdown)
        expected = [ParentNode("ul", [
            ParentNode("li", [LeafNode(None, "This is an unordered list")]),
            ParentNode("li", [LeafNode(None, "With multiple entries")]),
            ParentNode("li", [LeafNode(None, "It is valid")])
        ])]
        self.assertListEqual(expected, node)
        expected_html = '<ul><li>This is an unordered list</li><li>With multiple entries</li><li>It is valid</li></ul>'
        self.assertEqual(expected_html, node[0].to_html())
        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())

    def test_unordered_decor(self):
        markdown = "- This is an unordered list\n- With **multiple** entries\n- It is valid _with_ decor"
        node = block_to_block_node(markdown)
        expected = [ParentNode("ul", [
            ParentNode("li", [LeafNode(None, "This is an unordered list")]),
            ParentNode("li", [LeafNode(None, "With "), LeafNode("b", "multiple"), LeafNode(None, " entries")]),
            ParentNode("li", [LeafNode(None, "It is valid "), LeafNode("i", "with"), LeafNode(None, " decor")])
        ])]
        self.assertListEqual(expected, node)
        expected_html = '<ul><li>This is an unordered list</li><li>With <b>multiple</b> entries</li><li>It is valid <i>with</i> decor</li></ul>'
        self.assertEqual(expected_html, node[0].to_html())

        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())

    def test_ordered_plain(self):
        markdown = "1. This is an ordered list\n2. With multiple entries\n3. It is valid"
        node = block_to_block_node(markdown)
        expected = [ParentNode("ol", [
            ParentNode("li", [LeafNode(None, "This is an ordered list")]),
            ParentNode("li", [LeafNode(None, "With multiple entries")]),
            ParentNode("li", [LeafNode(None, "It is valid")])
        ])]
        self.assertListEqual(expected, node)
        expected_html = '<ol><li>This is an ordered list</li><li>With multiple entries</li><li>It is valid</li></ol>'
        self.assertEqual(expected_html, node[0].to_html())
        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())

    def test_ordered_decor(self):
        markdown = "- This is an ordered list\n- With **multiple** entries\n- It is valid _with_ decor"
        node = block_to_block_node(markdown)
        expected = [ParentNode("ul", [
            ParentNode("li", [LeafNode(None, "This is an ordered list")]),
            ParentNode("li", [LeafNode(None, "With "), LeafNode("b", "multiple"), LeafNode(None, " entries")]),
            ParentNode("li", [LeafNode(None, "It is valid "), LeafNode("i", "with"), LeafNode(None, " decor")])
        ])]
        self.assertListEqual(expected, node)
        expected_html = '<ul><li>This is an ordered list</li><li>With <b>multiple</b> entries</li><li>It is valid <i>with</i> decor</li></ul>'
        self.assertEqual(expected_html, node[0].to_html())

        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())

    def test_paragraph_plain(self):
        markdown = "This is just a simple text block without any decor\nbut it does have a line break"
        nodes = block_to_block_node(markdown)
        expected = [ParentNode("p", [
            LeafNode(None, "This is just a simple text block without any decor\nbut it does have a line break")
        ])]
        self.assertListEqual(expected, nodes)
        expected_html = '<p>This is just a simple text block without any decor\nbut it does have a line break</p>'
        self.assertEqual(expected_html, nodes[0].to_html())

        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())

    def test_paragraph_decorated(self):
        markdown = "This is just a simple text block _with_ syntax\nand it **does** have decor"
        nodes = block_to_block_node(markdown)
        expected = [ParentNode("p", [
            LeafNode(None, "This is just a simple text block "),
            LeafNode("i", "with"),
            LeafNode(None, " syntax\nand it "),
            LeafNode("b", "does"),
            LeafNode(None, " have decor")
        ])]
        self.assertListEqual(expected, nodes)
        expected_html = '<p>This is just a simple text block <i>with</i> syntax\nand it <b>does</b> have decor</p>'
        self.assertEqual(expected_html, nodes[0].to_html())

        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())

    def test_paragraph_link_image(self):
        markdown = "This is just a simple text block [with](example.com) a link\nand it **does** have an ![image](example.com/star.png)"
        nodes = block_to_block_node(markdown)
        expected = [ParentNode("p", [
            LeafNode(None, "This is just a simple text block "),
            LeafNode("a", "with", {"href": "example.com"}),
            LeafNode(None, " a link\nand it "),
            LeafNode("b", "does"),
            LeafNode(None, " have an "),
            LeafNode("img", "", {"src": "example.com/star.png", "alt": "image"})
        ])]
        self.assertListEqual(expected, nodes)
        expected_html = '<p>This is just a simple text block <a href="example.com">with</a> a link\nand it <b>does</b> have an <img src="example.com/star.png" alt="image" /></p>'
        self.assertEqual(expected_html, nodes[0].to_html())

        div = markdown_to_html(markdown)
        self.assertEqual(ParentNode("div", expected), div)
        self.assertEqual(f"<div>{expected_html}</div>", div.to_html())
    
    def test_big_markdown(self):
        div = markdown_to_html(self.block_md)
        expected = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "This is a "),
                LeafNode("b", "bolded"),
                LeafNode(None, " paragraph")]),
            ParentNode("p", [
                LeafNode(None, "This is another paragraph with "),
                LeafNode("i", "italic"),
                LeafNode(None, " text and "),
                LeafNode("code", "code"),
                LeafNode(None, " here\nThis is the same paragraph on a new line")]),
            ParentNode("h3", [
                LeafNode(None, "This is "),
                LeafNode("b", "a"), 
                LeafNode(None, " "),
                LeafNode("i", "header")]),
            LeafNode("code", "This is a code block\nacross two lines"),
            ParentNode("ol", [
                ParentNode("li", [
                    LeafNode(None, "This is an ordered list"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "With multiple items")
                ])
            ]),
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode(None, "This is an unordered list"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "with items")
                ])
            ]),
            ParentNode("blockquote", [
                LeafNode(None, "This is a quote\nThat goes onto two lines\n-Michael Scott")
            ])
        ])
        self.assertEqual(expected, div)
        self.assertEqual(expected.to_html(), div.to_html())

    def test_big_extra_line_markdown(self):
        div = markdown_to_html(self.block_extra_line_md)
        expected = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "This is a "),
                LeafNode("b", "bolded"),
                LeafNode(None, " paragraph")]),
            ParentNode("p", [
                LeafNode(None, "This is another paragraph with "),
                LeafNode("i", "italic"),
                LeafNode(None, " text and "),
                LeafNode("code", "code"),
                LeafNode(None, " here\nThis is the same paragraph on a new line")]),
            ParentNode("h3", [LeafNode(None, "This is a header")]),
            LeafNode("code", "This is a code block\nacross two lines"),
            ParentNode("ol", [
                ParentNode("li", [
                    LeafNode(None, "This is an ordered list"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "With multiple items")
                ])
            ]),
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode(None, "This is an unordered list"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "with items")
                ])
            ]),
            ParentNode("blockquote", [
                LeafNode(None, "This is a quote\nThat goes onto two lines\n-Michael Scott")
            ])
        ])
        self.assertEqual(expected, div)
        self.assertEqual(expected.to_html(), div.to_html())