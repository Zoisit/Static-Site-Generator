import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        n1 = HTMLNode()
        n2 = HTMLNode()
        self.assertEqual(n1, n2)

        n1 = HTMLNode("span", "Some text", [HTMLNode()], {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertNotEqual(n1, n2)
        n2 = HTMLNode("span", "Some text", [HTMLNode()], {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(n1, n2)

    def test_values(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

        node = HTMLNode("span", "Some text", [HTMLNode()], {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Some text")
        self.assertEqual(node.children, [HTMLNode()])
        self.assertEqual(node.props, {
            "href": "https://www.google.com",
            "target": "_blank",
        })

    def test_props_to_html(self):
        s1 = HTMLNode().props_to_html()
        s2 = ""
        self.assertEqual(s1, s2)
        
        s1 = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        }).props_to_html()
        s2 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(s1, s2)

        

    def test_repr(self):
        node = HTMLNode()
        repr = "HTMLNode(tag=None, value=None, children=None, props=None)"
        self.assertEqual(str(node), repr)

        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        repr = 'HTMLNode(tag=None, value=None, children=None, props=[ href="https://www.google.com" target="_blank"])'
        self.assertEqual(str(node), repr)
        
        node = HTMLNode("p", "Some text", [HTMLNode()], {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        repr = 'HTMLNode(tag="p", value="Some text", children=[HTMLNode(tag=None, value=None, children=None, props=None)], props=[ href="https://www.google.com" target="_blank"])'
        self.assertEqual(str(node), repr)

if __name__ == "__main__":
    unittest.main()