import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_equal_empty(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_equal_no_children(self):
        props = {"href":"boot.dev", "target":"_blank"}
        node = HTMLNode("p", "This is a paragraph", None, props)
        node2 = HTMLNode("p", "This is a paragraph", None, props)
        self.assertEqual(node, node2)

    def test_equal_full(self):
        props = {"href":"boot.dev", "target":"_blank"}
        props2 = {"href":"boot.dev"}
        child = HTMLNode("a", "This is a child", None, props2)
        node = HTMLNode("p", "This is a paragraph", child, props)
        node2 = HTMLNode("p", "This is a paragraph", child, props)
        self.assertEqual(node, node2)

    def test_repr(self):
        props = {"href":"boot.dev", "target":"_blank"}
        props2 = {"href":"boot.dev"}
        child = HTMLNode("a", "This is a child", None, props2)
        node = HTMLNode("p", "This is a paragraph", child, props)
        expected = 'HTMLNode(p, This is a paragraph, HTMLNode(a, This is a child, None, href="boot.dev"), href="boot.dev" target="_blank")'
        self.assertEqual(str(node), expected)

    def test_equal_multiple_children(self):
        # Test equality with multiple children
        child1 = HTMLNode("span", "Child 1")
        child2 = HTMLNode("span", "Child 2")
        children = [child1, child2]
        node1 = HTMLNode("div", "Parent", children)
        node2 = HTMLNode("div", "Parent", [HTMLNode("span", "Child 1"), HTMLNode("span", "Child 2")])
        self.assertEqual(node1, node2)

    def test_equal_deeply_nested(self):
        # Test equality with deeply nested children
        deep_child = HTMLNode("em", "Deep")
        child = HTMLNode("span", "Child", deep_child)
        parent = HTMLNode("div", "Parent", child)
        deep_child2 = HTMLNode("em", "Deep")
        child2 = HTMLNode("span", "Child", deep_child2)
        parent2 = HTMLNode("div", "Parent", child2)
        self.assertEqual(parent, parent2)

    def test_repr_multiple_children(self):
        # Test string representation with multiple children
        child1 = HTMLNode("li", "Item 1")
        child2 = HTMLNode("li", "Item 2")
        children = [child1, child2]
        node = HTMLNode("ul", None, children)
        expected = 'HTMLNode(ul, None, [HTMLNode(li, Item 1, None, None), HTMLNode(li, Item 2, None, None)], None)'
        self.assertEqual(str(node), expected)

    def test_repr_deeply_nested(self):
        # Test string representation with deeply nested children
        deep_child = HTMLNode("b", "Bold")
        child = HTMLNode("span", "Child", deep_child)
        node = HTMLNode("div", "Parent", child)
        expected = 'HTMLNode(div, Parent, HTMLNode(span, Child, HTMLNode(b, Bold, None, None), None), None)'
        self.assertEqual(str(node), expected)

    def test_props_to_html(self):
        props = {"href":"boot.dev", "target":"_blank"}
        node = HTMLNode("p", "This is a paragraph", None, props)
        result = node.props_to_html()
        expected = 'href="boot.dev" target="_blank"'
        self.assertEqual(result, expected)
        
    def test_props_empty_to_html(self):
        props = {}
        node = HTMLNode("p", "This node has empty props", props=props)
        results = node.props_to_html()
        expected = None
        self.assertEqual(expected, results)
        
    def test_props_none_to_html(self):
        node = HTMLNode("p", "This node has None props", props=None)
        result = node.props_to_html()
        expected = None
        self.assertEqual(result, expected)

    def test_props_special_to_html(self):
        props = {"href": "example\n.com"}
        node = HTMLNode("p", "This is a paragraph", None, props)
        result = node.props_to_html()
        expected = 'href="example\n.com"'
        self.assertEqual(result, expected)
        
    def test_not_equal(self):
        props = {"href":"boot.dev", "target":"_blank"}
        node = HTMLNode("p", "This is a paragraph", None, props)
        node2 = HTMLNode("a", "link", None, None)
        self.assertNotEqual(node, node2)
        
    def test_not_equal_similar(self):
        props = {"href":"boot.dev", "target":"_blank"}
        props2 = {"href":"boot..dev", "target":"_blank"}
        node = HTMLNode("p", "This is a paragraph", None, props)
        node2 = HTMLNode("p", "This is a paragraph", None, props2)
        self.assertNotEqual(node, node2)

    def test_not_equal_diff_obj(self):
        node = HTMLNode("a", "link", None, None)
        self.assertFalse(node == "test")