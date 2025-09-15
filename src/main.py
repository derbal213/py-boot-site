import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from functions.extract_markdown import extract_markdown_images, extract_markdown_links
from functions.text_to_text_nodes import text_to_text_nodes
from functions.file_handler import copy_files

def main():
    # names = [
    # "tests.test_markdown_to_html.TestMarkdownToHTML.test_ordered_plain"
    # ]
    # suite = unittest.TestLoader().loadTestsFromNames(names)
    # unittest.TextTestRunner().run(suite)

    src = "/Users/derekball/Library/Mobile Documents/com~apple~CloudDocs/Mailbox Cloud Drive/OX Drive/My files.localized/Programming/git/py-boot-site/static"
    dest = "/Users/derekball/Library/Mobile Documents/com~apple~CloudDocs/Mailbox Cloud Drive/OX Drive/My files.localized/Programming/git/py-boot-site/public"
    copy_files(src, dest)
    
if __name__ == "__main__":
    main()