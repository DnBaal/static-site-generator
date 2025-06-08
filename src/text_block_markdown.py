import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TextBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_line(self):
        md = "This is a single line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line"])

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_trailing_spaces_and_newlines(self):
        md = "This is a paragraph with trailing spaces and newlines    \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["This is a paragraph with trailing spaces and newlines"]
        )

    def test_markdown_to_blocks_indented_newlines(self):
        md = """
This is **bolded** paragraph
                                
        
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
             
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_ord(self):
        block = """1. This is ordered list
2. second part
3. third part"""
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.OLIST, block_type)

    def test_block_to_block_type_heading(self):
        block = """# This is a heading
this is second line
and third one
"""
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> one more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- unord list item\n- second list item"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. ordlist\n2. second item"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        md = "### three heading hello!"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>three heading hello!</h3></div>")

    def test_headings(self):
        md = """
# This is an h1

this is paragraph

## this is an h2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is an h1</h1><p>this is paragraph</p><h2>this is an h2</h2></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote(self):
        md = """
>This is **bolded** quote
>text in a p
>tag here
>This is another line of quote with _italic_ text and `code` here

this is paragraph after quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is <b>bolded</b> quote text in a p tag here This is another line of quote with <i>italic</i> text and <code>code</code> here</p></blockquote><p>this is paragraph after quote</p></div>",
        )

    def test_blockquote_quotes(self):
        md = """
>This is **bolded** quote paragraph
>text in a p
>tag here
>
>This is another quote paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is <b>bolded</b> quote paragraph text in a p tag here</p><p>This is another quote paragraph with <i>italic</i> text and <code>code</code> here</p></blockquote></div>",
        )

    def test_lists(self):
        md = """
- This  is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This  is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_ulist(self):
        md = """
- This is **bolded** quote paragraph
- text in a p
- tag here
- This is another item of quote with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is <b>bolded</b> quote paragraph</li><li>text in a p</li><li>tag here</li><li>This is another item of quote with <i>italic</i> text and <code>code</code> here</li></ul></div>",
        )

    def test_olist(self):
        md = """
1. This is **bolded** paragraph
2. text in a p
3. tag here
4. This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is <b>bolded</b> paragraph</li><li>text in a p</li><li>tag here</li><li>This is another paragraph with <i>italic</i> text and <code>code</code> here</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
