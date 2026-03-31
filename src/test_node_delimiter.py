import unittest

from textnode import TextNode, TextType
from node_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from extract_markdown import extract_markdown_images, extract_markdown_links

class Test_Split_Nodes_Delimiter(unittest.TestCase):
    def test_0(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, result)

    def test_1(self):
        node = TextNode("**bolded phrase_0**This is text with a **bolded phrase_1** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = [
            TextNode("bolded phrase_0", TextType.BOLD),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase_1", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(new_nodes, result)

    def test_2(self):
        node = TextNode("__This is text with a _italic phrase-0_ word _italic phrase-1_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic phrase-0", TextType.ITALIC),
            TextNode(" word ", TextType.TEXT),
            TextNode("italic phrase-1", TextType.ITALIC),
            ]
        self.assertEqual(new_nodes, result)


class Test_extract_markdown(unittest.TestCase):
    def test_img_0(self):
        matches = extract_markdown_images(
             "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
         )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_iink_0(self):
        matches = extract_markdown_links(
             "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
         )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_iink_1(self):
        matches = extract_markdown_links(
             "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [another_link](https://i.imgur.com/owowowo.png)"
         )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"),("another_link", "https://i.imgur.com/owowowo.png")], matches)


class Test_split_nodes(unittest.TestCase):
    def test_split_images_0(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and an ending text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and an ending text", TextType.TEXT),

            ],
            new_nodes,
        )

    def test_split_links_0(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),

            ],
            new_nodes,
        )

    def test_split_links_1(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) start with link [to youtube](https://www.youtube.com/@bootdotdev) end with text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" start with link ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(" end with text", TextType.TEXT),

            ],
            new_nodes,
        )

class Test_text_to_textnodes(unittest.TestCase):
    def test_text_to_textnodes_1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    