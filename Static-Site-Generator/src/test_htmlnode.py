import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_props_to_html_None(self):
        s1 = HTMLNode().props_to_html()
        s2 = ""
        self.assertEqual(s1, s2)

    def test_props_to_html(self):
        s1 = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        }).props_to_html()
        s2 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(s1, s2)


    def test_repr_empty(self):
        node = HTMLNode()
        repr = "HTMLNode(tag=None, value=None, children=None, props=None)"
        self.assertEqual(str(node), repr)

    def test_repr_props(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        repr = 'HTMLNode(tag=None, value=None, children=None, props=[ href="https://www.google.com" target="_blank"])'
        self.assertEqual(str(node), repr)

    def test_repr(self):
        node = HTMLNode("p", "Some text", [HTMLNode()], {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        repr = 'HTMLNode(tag="p", value="Some text", children=[HTMLNode(tag=None, value=None, children=None, props=None)], props=[ href="https://www.google.com" target="_blank"])'
        self.assertEqual(str(node), repr)

if __name__ == "__main__":
    unittest.main()