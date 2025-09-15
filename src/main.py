import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from functions.extract_markdown import extract_markdown_images, extract_markdown_links
from functions.text_to_text_nodes import text_to_text_nodes

def main():
    names = [
    "tests.test_markdown_to_html.TestMarkdownToHTML.test_ordered_plain"
    ]
    suite = unittest.TestLoader().loadTestsFromNames(names)
    unittest.TextTestRunner().run(suite)

    
if __name__ == "__main__":
    main()