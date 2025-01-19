import unittest

from parentnode import ParentNode
from leafnode import LeafNode
from htmlnode import HTMLNode


class TestParentNode(unittest.TestCase):
    def test_values(self):
        node = ParentNode(None, None)
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

        node = ParentNode("span", [], {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {
            "href": "https://www.google.com",
            "target": "_blank",
        })

        node = ParentNode("div", [ParentNode("p", []), LeafNode("a", "www.test.de"), HTMLNode()])
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [ParentNode("p", []), LeafNode("a", "www.test.de"), HTMLNode()])
        self.assertEqual(node.props, None)
    
    def test_to_html(self):
        node = ParentNode(None, None)
        with self.assertRaises(Exception) as context:
            node.to_html()
        self.assertTrue("All parent nodes must have a tag" in str(context.exception))

        node = ParentNode("img", None)
        with self.assertRaises(Exception) as context:
            node.to_html()
        self.assertTrue("All parent nodes must have a least one child" in str(context.exception))

        node = ParentNode("p", [])
        self.assertEqual(node.to_html(), "<p></p>")


        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("div", [LeafNode("i", "italic text"), LeafNode(None, "Normal text")]),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b><div><i>italic text</i>Normal text</div>Normal text</p>")

if __name__ == "__main__":
    unittest.main()