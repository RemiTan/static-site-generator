class HTMLNode:
    def __init__(
        self,
        value: str = None,
        tag: str = None,
        children: list["HTMLNode"] = None,
        props: dict[str, str] = None,
    ) -> None:
        self.value = value
        self.tag = tag
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
        value: str,
        tag: str = None,
        props: dict[str, str] = None,
    ) -> None:
        super().__init__(value, tag, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
