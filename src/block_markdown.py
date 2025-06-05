import re
from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                grandchildren = text_to_children(block)
                parent_node = ParentNode("p", grandchildren)
                children.append(parent_node)

            case BlockType.HEADING:
                match = re.match(r"^(#{1,6})\s(.*)", block)
                if match:
                    heading_type = match.group(1)
                    text = match.group(2)
                    grandchildren = text_to_children(text)
                    parent_node = ParentNode(f"h{len(heading_type)}", grandchildren)
                    children.append(parent_node)

            case BlockType.CODE:
                match = re.search(r"```\n(.*?)```", block, re.DOTALL)
                if match:
                    text = match.group(1)
                    code_node = TextNode(text, TextType.CODE)
                    parent_node = ParentNode("pre", [text_node_to_html_node(code_node)])
                    children.append(parent_node)

            case BlockType.QUOTE:
                lines = block.split(">")
                quote = ""
                grandchildren = []
                for line in lines:
                    if line == "\n" and quote:
                        p_children = text_to_children(quote)
                        grandchildren.append(ParentNode("p", p_children))
                        quote = ""
                        continue
                    quote += line
                if quote:
                    p_children = text_to_children(quote)
                    grandchildren.append(ParentNode("p", p_children))
                children.append(ParentNode("quoteblock", grandchildren))

            case BlockType.ULIST:
                lines = block.split("- ")
                grandchildren = []
                for line in lines:
                    if line:
                        li_children = text_to_children(line)
                        grandchildren.append(ParentNode("li", li_children))
                children.append(ParentNode("ul", grandchildren))

            case BlockType.OLIST:
                lines = re.split(r"\d+\.\s", block)
                grandchildren = []
                for line in lines:
                    if line:
                        li_children = text_to_children(line)
                        grandchildren.append(ParentNode("li", li_children))
                children.append(ParentNode("ol", grandchildren))

    div_parent = ParentNode("div", children)
    return div_parent


def text_to_children(text):
    text = text.replace("\n", " ").strip()
    children = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        children.append(text_node_to_html_node(textnode))
    return children


def markdown_to_blocks(markdown):
    fixed_blocks = []
    blocks = re.split(r"\n\s*\n", markdown)
    for block in blocks:
        if not block:
            continue
        block = block.strip()
        fixed_blocks.append(block)

    return fixed_blocks


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for quote in lines:
            if not quote.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    if block.startswith("1. "):
        for i in range(1, len(lines) + 1):
            if not lines[i - 1].startswith(f"{i}. "):
                return BlockType.PARAGRAPH
        return BlockType.OLIST

    return BlockType.PARAGRAPH
