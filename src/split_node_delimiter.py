from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)
        if not (len(sections) % 2):
            raise ValueError("Invalid markdown, formatted section not closed")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            text_node = (
                TextNode(sections[i], TextType.TEXT)
                if i % 2 == 0
                else TextNode(sections[i], text_type)
            )
            new_nodes.append(text_node)

    return new_nodes
