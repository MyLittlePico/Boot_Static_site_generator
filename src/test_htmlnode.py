import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node.props_to_html(),node2.props_to_html())
    def test_props_to_html1(self):
        prop = {"href": "https://www.google.com",
                "target": "_blank",
        }
        node = HTMLNode(props = prop)
        node2 = HTMLNode(props = prop)
        self.assertEqual(node.props_to_html(),node2.props_to_html())
    def test_props_to_html2(self):
        prop = {"href": "https://www.google.com",
                "target": "_blank",
        }
        node = HTMLNode(props = prop)
        node2 = HTMLNode(props = "what")
        self.assertNotEqual(node.props_to_html(),node2.props_to_html())
    def test_props_to_html3(self):
        prop = {"href": "https://www.google.com",
                "target": "_blank",
        }
        node = HTMLNode(props = prop)
        node2 = HTMLNode(props = None)
        self.assertNotEqual(node.props_to_html(),node2.props_to_html())


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html1(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html2(self):
        node = LeafNode(None, "Hello, world!", )
        self.assertEqual(node.to_html(), "Hello, world!")

class TextParentNode(unittest.TestCase):
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