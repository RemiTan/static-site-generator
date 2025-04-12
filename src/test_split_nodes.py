import unittest

from split_nodes import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitDelimiterNode(unittest.TestCase):
    def test_text_split_with_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        nodes = split_nodes_delimiter([node], "`")

        self.assertEqual(nodes, expected_nodes)

    def test_text_split_with_bold_block(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        nodes = split_nodes_delimiter([node], "**")

        self.assertEqual(nodes, expected_nodes)

    def test_text_split_with_italic_block(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        nodes = split_nodes_delimiter([node], "_")

        self.assertEqual(nodes, expected_nodes)

    def test_chaining_text_split_with_italic_block_and_bold_block(self):
        node = TextNode("_italic block_ and **bold block**", TextType.TEXT)

        expected_nodes = [
            TextNode("italic block", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
        ]

        nodes = split_nodes_delimiter([node], "_")
        nodes = split_nodes_delimiter(nodes, "**")

        self.assertEqual(nodes, expected_nodes)

    def test_text_split_skip_not_text_block(self):
        node = TextNode("This is text with a _italic block_ word", TextType.BOLD)

        expected_nodes = [node]

        nodes = split_nodes_delimiter([node], "_")

        self.assertEqual(nodes, expected_nodes)

    def test_text_split_raise_error_syntax(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)

        with self.assertRaisesRegex(ValueError, "Invalid Markdown syntax delimiter."):
            split_nodes_delimiter([node], "*")

    def test_text_split_multiple_bold_blocks(self):
        node = TextNode(
            "This is text with a **bold block** word and a second **bold block**",
            TextType.TEXT,
        )

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word and a second ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
        ]

        nodes = split_nodes_delimiter([node], "**")

        self.assertEqual(nodes, expected_nodes)

    def test_text_split_multiple_bold_blocks_edge_case(self):
        node = TextNode(
            "This is text with a **bold block****bold block**",
            TextType.TEXT,
        )

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode("bold block", TextType.BOLD),
        ]

        nodes = split_nodes_delimiter([node], "**")

        self.assertEqual(nodes, expected_nodes)

        node = TextNode(
            "This is text with a ********",
            TextType.TEXT,
        )

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
        ]

        nodes = split_nodes_delimiter([node], "**")

        self.assertEqual(nodes, expected_nodes)

    def test_text_split_raise_error_unclosing_delimiter(self):
        node = TextNode(
            "This is text with a **bold block** word and a second **bold block",
            TextType.TEXT,
        )

        with self.assertRaisesRegex(Exception, "Unclosing delimiter issue."):
            split_nodes_delimiter([node], "**")

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_same_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_no_match_link(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        expected_nodes = [node]
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_same_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_not_matching_images(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        expected_nodes = [node]
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, expected_nodes)

    def test_chaining_split_nodes_with_link_and_image(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) and ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(new_nodes, expected_nodes)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_matches = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        matches = extract_markdown_images(text)
        self.assertEqual(matches, expected_matches)

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected_matches = [("image", "https://i.imgur.com/zjjcJKZ.png")]

        matches = extract_markdown_images(text)
        self.assertListEqual(matches, expected_matches)

    def test_extract_markdown_images_no_match(self):
        text = "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        expected_matches = []

        matches = extract_markdown_images(text)
        self.assertListEqual(matches, expected_matches)

    def test_extract_markdown_links(self):
        text = "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        expected_matches = [("link", "https://i.imgur.com/zjjcJKZ.png")]

        matches = extract_markdown_links(text)
        self.assertListEqual(matches, expected_matches)

    def test_extract_markdown_links_no_match(self):
        text = "This is text with an ![link](https://i.imgur.com/zjjcJKZ.png)"
        expected_matches = []

        matches = extract_markdown_links(text)
        self.assertListEqual(matches, expected_matches)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, expected_nodes)
