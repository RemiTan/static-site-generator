import unittest

from htmlnode import HTMLNode, LeafNode


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
        node = LeafNode("Hello world!", "p")
        self.assertEqual(
            str(node),
            "HTMLNode(tag=p, value=Hello world!, children=None, props=None)",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("Hello world!", "p")
        self.assertEqual(node.to_html(), "<p>Hello world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("Click me!", "a", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_with_no_tag(self):
        node = LeafNode("test")
        self.assertEqual(node.to_html(), "test")

    def test_leaf_to_html_with_no_value(self):
        with self.assertRaisesRegex(ValueError, "All leaf nodes must have a value."):
            LeafNode(value=None).to_html()
