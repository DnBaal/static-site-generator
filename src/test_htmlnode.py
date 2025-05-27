import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "one", "value", {"href": 2})
        self.assertEqual("HTMLNode(p, one, value, {'href': 2})", repr(node))

    def test_props_to_html(self):
        node = HTMLNode("p", "one", None, {"href": 2, "target": "_blank"})
        self.assertEqual(' href="2" target="_blank"', node.props_to_html())

    def test_none_atrbts(self):
        node = HTMLNode("p", "one", "value")
        self.assertEqual("HTMLNode(p, one, value, None)", repr(node))

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish i could do rust",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish i could do rust",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("div", "checking this shit")
        self.assertEqual("<div>checking this shit</div>", node.to_html())

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "checking this shit", {"href": "https:pyright.com"})
        self.assertEqual(
            '<a href="https:pyright.com">checking this shit</a>', node.to_html()
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "hello")
        self.assertEqual(node.to_html(), "hello")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Bold text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>Italic text</i>Bold text</h2>",
        )

    def test_to_html_many_children_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node1 = ParentNode("span", [grandchild_node])
        child_node2 = LeafNode("span", "blue", {"color": "blue"})
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b>grandchild</b></span><span color="blue">blue</span></div>',
        )
