import unittest
from functions.extract_markdown import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected, matches)

    def test_extract_multiple_images(self):
        text = "![one](url1) and ![two](url2)"
        expected = [("one", "url1"), ("two", "url2")]
        matches = extract_markdown_images(text)
        self.assertListEqual(expected, matches)

    def test_extract_single_link(self):
        text = "[one](url1)"
        expected = [("one", "url1")]
        matches = extract_markdown_links(text)
        self.assertListEqual(expected, matches)

    def test_extract_spaced_txt_image(self):
        text = "![my cool image](http://img.com/cool.png)"
        expected = [("my cool image", "http://img.com/cool.png")]
        matches = extract_markdown_images(text)
        self.assertListEqual(expected, matches)
    
    def test_extract_no_images(self):
        text = "This text has no markdown image"
        expected = []
        matches = extract_markdown_images(text)
        self.assertListEqual(expected, matches)

    def test_extract_img_in_sentence(self):
        text = "Check this out (![wow](url))."
        expected = [("wow", "url")]
        matches = extract_markdown_images(text)
        self.assertListEqual(expected, matches)

    def test_extract_img_empty_txt(self):
        text = "![](http://example.com/no-alt.png)"
        expected = [("", "http://example.com/no-alt.png")]
        matches = extract_markdown_images(text)
        self.assertListEqual(expected, matches)

    def test_extract_img_empty_url(self):
        text = "![alt]()"
        expected = [("alt", "")]
        matches = extract_markdown_images(text)
        self.assertListEqual(expected, matches)

    def test_extract_img_empty(self):
        text = "![]()"
        expected = [("", "")]
        matches = extract_markdown_images(text)
        self.assertListEqual(expected, matches)

    def test_extract_spaced_txt_link(self):
        text = "[my cool link](http://img.com/cool.png)"
        expected = [("my cool link", "http://img.com/cool.png")]
        matches = extract_markdown_links(text)
        self.assertListEqual(expected, matches)
    
    def test_extract_no_links(self):
        text = "This text has no links"
        expected = []
        matches = extract_markdown_links(text)
        self.assertListEqual(expected, matches)

    def test_extract_link_in_sentence(self):
        text = "Check this out ([wow](url))."
        expected = [("wow", "url")]
        matches = extract_markdown_links(text)
        self.assertListEqual(expected, matches)

    def test_extract_link_empty_txt(self):
        text = "[](http://example.com/no-alt.png)"
        expected = [("", "http://example.com/no-alt.png")]
        matches = extract_markdown_links(text)
        self.assertListEqual(expected, matches)

    def test_extract_link_empty_url(self):
        text = "[alt]()"
        expected = [("alt", "")]
        matches = extract_markdown_links(text)
        self.assertListEqual(expected, matches)

    def test_extract_link_empty(self):
        text = "[]()"
        expected = [("", "")]
        matches = extract_markdown_links(text)
        self.assertListEqual(expected, matches)

    def test_extract_image_not_link(self):
        text = "Check this out ([wow](url))."
        expected = []
        matches = extract_markdown_images(text)
        self.assertListEqual(expected, matches)

    def test_extract_link_not_img(self):
        text = "Check this out (![wow](url))."
        expected = []
        matches = extract_markdown_links(text)
        self.assertListEqual(expected, matches)

    def test_extract_both(self):
        text = "This is a [sentence](url) with both [links](url2) and images! ![cool](http://img.com/cool.png) ![happy](http://img.com/happy.png)"
        expected_links = [("sentence", "url"), ("links", "url2")]
        expected_imgs = [("cool", "http://img.com/cool.png"), ("happy", "http://img.com/happy.png")]
        matched_links = extract_markdown_links(text)
        matched_imgs = extract_markdown_images(text)
        self.assertListEqual(expected_links, matched_links)
        self.assertListEqual(expected_imgs, matched_imgs)

