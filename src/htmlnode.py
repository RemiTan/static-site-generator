from textnode import TextType


class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list["HTMLNode"] = None,
        props: dict[str, str] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""

        html = ""
        for key, value in self.props.items():
            html += f' {key}="{value}"'
        return html

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: dict[str, str] = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str] = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")

        if self.children is None:
            raise ValueError("All parent nodes must have an attributed children value.")
        html_children = ""
        for child in self.children:
            html_children += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{html_children}</{self.tag}>"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img", "", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError("text_type doesn't correspond to any of TextType.")
