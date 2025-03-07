import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_create_html_node(self):
        html_node = HTMLNode(
            tag="p",
            value="Hello world!",
            children=[],
            props={"href": "www.test.com"},
        )

        self.assertEqual(html_node.tag, "p")
        self.assertEqual(html_node.value, "Hello world!")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {"href": "www.test.com"})

    def test_create_empty_html_node(self):
        html_node = HTMLNode()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_repr_html_node(self):
        html_node = HTMLNode(
            tag="p",
            value="Hello world!",
            children=[],
            props={"href": "www.test.com"},
        )
        self.assertEqual(
            str(html_node),
            "HTMLNode(tag=p, value=Hello world!, children=[], props={'href': 'www.test.com'})",
        )

    def test_raise_error_to_html(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()


class TestLeafNode(unittest.TestCase):
    def test_create_leaf_node(self):
        node = LeafNode("p", "Hello world!")
        self.assertEqual(
            str(node),
            "HTMLNode(tag=p, value=Hello world!, children=None, props=None)",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello world!")
        self.assertEqual(node.to_html(), "<p>Hello world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_with_no_tag(self):
        node = LeafNode(None, "test")
        self.assertEqual(node.to_html(), "test")

    def test_leaf_to_html_with_no_value(self):
        with self.assertRaisesRegex(ValueError, "All leaf nodes must have a value."):
            LeafNode(tag="p", value=None).to_html()


class TestParentNode(unittest.TestCase):
    def test_parent_node_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_parent_node_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_node_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_to_html_with_no_tag(self):
        with self.assertRaisesRegex(ValueError, "All parent nodes must have a tag."):
            ParentNode(None, []).to_html()

    def test_parent_node_to_html_with_no_defined_children(self):
        with self.assertRaisesRegex(
            ValueError, "All parent nodes must have an attributed children."
        ):
            ParentNode("b", None).to_html()

    def test_parent_node_to_html_with_issue_children(self):
        with self.assertRaisesRegex(ValueError, "All leaf nodes must have a value."):
            LeafNode("b", None).to_html()


class TestConvertTextNodeToHMLTNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("test", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "test")

    def test_italic_text(self):
        node = TextNode("test", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "test")

    def test_code_text(self):
        node = TextNode("test", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "test")

    def test_link_text(self):
        node = TextNode("test", TextType.LINK, "some url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "test")
        self.assertEqual(html_node.props, {"href": "some url"})

    def test_image_text(self):
        node = TextNode("test", TextType.IMAGE, "some url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "some url", "alt": "test"})

    def test_raise_error_text_type(self):
        node = TextNode("test", "bad")
        with self.assertRaisesRegex(
            ValueError, "text_type doesn't correspond to any of TextType."
        ):
            text_node_to_html_node(node)
