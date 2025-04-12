import re
from collections.abc import Callable

from textnode import TextNode, TextType

MATCHING_DELIMITER = {
    "**": TextType.BOLD,
    "_": TextType.ITALIC,
    "`": TextType.CODE,
}


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
) -> list[TextNode]:
    if delimiter not in MATCHING_DELIMITER:
        raise ValueError("Invalid Markdown syntax delimiter.")
    text_type = MATCHING_DELIMITER[delimiter]

    nodes_list = []
    for _node in old_nodes:
        if _node.text_type != TextType.TEXT:
            nodes_list.append(_node)
            continue

        splitted_text = _node.text.split(delimiter)

        if len(splitted_text) % 2:
            for i, _text in enumerate(splitted_text):
                if _text == "":
                    continue

                if i % 2 == 0:
                    nodes_list.append(TextNode(_text, TextType.TEXT))
                else:
                    nodes_list.append(TextNode(_text, text_type))
        else:
            raise Exception("Unclosing delimiter issue.")

    return nodes_list


def extract_markdown_images(text: str) -> tuple[str, str]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> tuple[str, str]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]):
    return split_nodes_with_extract_func(
        old_nodes,
        extract_markdown_images,
        "![{}]({})",
        TextType.IMAGE,
    )


def split_nodes_link(old_nodes: list[TextNode]):
    return split_nodes_with_extract_func(
        old_nodes,
        extract_markdown_links,
        "[{}]({})",
        TextType.LINK,
    )


def split_nodes_with_extract_func(
    old_nodes: list[TextNode],
    extract_func: Callable,
    match_string: str,
    text_type: TextType,
) -> list[TextNode]:
    nodes_list = []
    for _node in old_nodes:
        original_text = _node.text
        matches = extract_func(original_text)
        if not matches:
            nodes_list.append(_node)
            continue

        for text, link in matches:
            sections = original_text.split(
                match_string.format(text, link),
                1,
            )
            if sections[0] != "":
                nodes_list.append(TextNode(sections[0], TextType.TEXT))
            nodes_list.append(TextNode(text, text_type, link))
            original_text = sections[-1]
        else:
            if original_text != "":
                nodes_list.append(TextNode(original_text, TextType.TEXT))

    return nodes_list


def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]

    for delimiter in ["`", "**", "_"]:
        nodes = split_nodes_delimiter(nodes, delimiter)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
