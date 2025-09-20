import unittest
from src.parentnode import ParentNode
from src.leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError) as cm1:
            ParentNode("p", None).to_html()
        self.assertIn("Must include children", str(cm1.exception))

        node2 = ParentNode("div", [])
        with self.assertRaises(ValueError) as cm2:
            node2.to_html()
        self.assertIn("Must include children", str(cm2.exception))

    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError) as cm1:
            ParentNode(None, None).to_html()
        self.assertIn("Must include a tag", str(cm1.exception))

    def test_to_html_multiple_leafs(self):
        child1 = LeafNode("a", "This is a link", {"href":"boot.dev", "target": "_blank"})
        child2 = LeafNode("b", "This is bold text")
        parent_node = ParentNode("p", [child1, child2], {"title":"This is a paragraph"})
        expected = '<p title="This is a paragraph"><a href="boot.dev" target="_blank">This is a link</a><b>This is bold text</b></p>'
        actual = parent_node.to_html()
        self.assertEqual(expected, actual)

    def test_to_html_multiple_parents_leafs(self):
        child1 = LeafNode("a", "This is a link", {"href":"boot.dev", "target": "_blank"})
        child2 = LeafNode("b", "This is bold text")
        parent_node = ParentNode("p", [child1, child2], {"title":"This is a paragraph"})
        parent_parent = ParentNode("div", [parent_node])
        expected = '<div><p title="This is a paragraph"><a href="boot.dev" target="_blank">This is a link</a><b>This is bold text</b></p></div>'
        actual = parent_parent.to_html()
        self.assertEqual(expected, actual)

    def test_to_html_with_props(self):
        child = LeafNode("p", "text")
        parent = ParentNode("section", [child], props={"class": "main", "id": "s1"})

        result = parent.to_html()
        self.assertTrue(result.startswith("<section "))
        self.assertIn('class="main"', result)
        self.assertIn('id="s1"', result)
        self.assertTrue(result.endswith("</section>"))
        self.assertIn("<p>text</p>", result)