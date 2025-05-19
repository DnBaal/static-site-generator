import unittest

from htmlnode import HTMLNode


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
