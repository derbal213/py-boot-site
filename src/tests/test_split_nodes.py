import unittest
from functions.split_nodes import split_nodes_delimiter, split_nodes_image_and_links
from functions.text_to_html import text_nodes_to_leaf_nodes
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
            self.assertEqual(expected, parent_node.to_html())

    def test_split_img(self):
        node = TextNode("This is a text node with an image ![alt text](www.google.com/test.png)", TextType.PLAIN)
        new_nodes = split_nodes_image_and_links([node])
        self.assertEqual(2, len(new_nodes))
        leaf_nodes = text_nodes_to_leaf_nodes(new_nodes)
        self.assertEqual(2, len(leaf_nodes))

        parent_node = ParentNode("p", leaf_nodes)
        expected = '<p>This is a text node with an image <img src="www.google.com/test.png" alt="alt text" /></p>'
        actual = parent_node.to_html()
        self.assertEqual(expected, actual)

    def test_split_link(self):
        node = TextNode("This is a text node with a link [alt text](www.google.com/test.png)", TextType.PLAIN)
        new_nodes = split_nodes_image_and_links([node])
        self.assertEqual(2, len(new_nodes))
        leaf_nodes = text_nodes_to_leaf_nodes(new_nodes)
        self.assertEqual(2, len(leaf_nodes))

        parent_node = ParentNode("p", leaf_nodes)
        expected = '<p>This is a text node with a link <a href="www.google.com/test.png">alt text</a></p>'
        actual = parent_node.to_html()
        self.assertEqual(expected, actual)

    def test_split_multiple_img(self):
        node = TextNode("This is a text node ![first image](example.com/test.png) with two images ![alt text](www.google.com/test.png)", TextType.PLAIN)
        new_nodes = split_nodes_image_and_links([node])
        self.assertEqual(4, len(new_nodes))
        leaf_nodes = text_nodes_to_leaf_nodes(new_nodes)
        self.assertEqual(4, len(leaf_nodes))

        parent_node = ParentNode("p", leaf_nodes)
        expected = '<p>This is a text node <img src="example.com/test.png" alt="first image" /> with two images <img src="www.google.com/test.png" alt="alt text" /></p>'
        actual = parent_node.to_html()
        self.assertEqual(expected, actual)

    def test_split_multiple_links(self):
        node = TextNode("This is a text [node](example.com) with two links [alt text](www.google.com)", TextType.PLAIN)
        new_nodes = split_nodes_image_and_links([node])
        self.assertEqual(4, len(new_nodes))
        leaf_nodes = text_nodes_to_leaf_nodes(new_nodes)
        self.assertEqual(4, len(leaf_nodes))

        parent_node = ParentNode("p", leaf_nodes)
        expected = '<p>This is a text <a href="example.com">node</a> with two links <a href="www.google.com">alt text</a></p>'
        actual = parent_node.to_html()
        self.assertEqual(expected, actual)

    def test_split_links_and_imgs(self):
        node = TextNode("This is a [sentence](url) with both [links](url2) and images! ![cool](http://img.com/cool.png) ![happy](http://img.com/happy.png)", TextType.PLAIN)
        new_nodes = split_nodes_image_and_links([node])
        self.assertEqual(8, len(new_nodes))
        leaf_nodes = text_nodes_to_leaf_nodes(new_nodes)
        self.assertEqual(8, len(leaf_nodes))

        parent_node = ParentNode("p", leaf_nodes)
        expected = f'<p>This is a <a href="url">sentence</a> with both <a href="url2">links</a> and images! <img src="http://img.com/cool.png" alt="cool" /> <img src="http://img.com/happy.png" alt="happy" /></p>'
        actual = parent_node.to_html()
        self.assertEqual(expected, actual)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image_and_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )