import unittest

from textnode import TextNode, TextType,text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq1(self):
        node = TextNode("This is a text node", TextType.BOLD, url = None)
        node2 = TextNode("This is a text node", TextType.BOLD, url = "gg")
        self.assertNotEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_eq3(self):
        node = TextNode("This is a url node", TextType.LINK, url = "gg")
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)


class TextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_text1(self):
        node = TextNode("This is a anchor text", TextType.LINK, "This is a url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a anchor text")
        self.assertEqual(html_node.props["href"], "This is a url") 
    def test_text2(self):
        node = TextNode("This is alt text", TextType.IMAGE,"This is a url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "This is a url") 
        self.assertEqual(html_node.props["alt"], "This is alt text") 




if __name__ == "__main__":
    unittest.main()


