import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_values(self):
        node = LeafNode(None, None)
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

        node = LeafNode("span", "Some text", {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Some text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
    
    def test_to_html(self):
        node = LeafNode(None, None)
        with self.assertRaises(Exception) as context:
            node.to_html()
        self.assertTrue("All leaf nodes must have a value" in str(context.exception))

        node = LeafNode(None, "LeafNode value")
        self.assertTrue(node.to_html(), "LeafNode value")

        node = LeafNode("p", "LeafNode value")
        self.assertTrue(node.to_html(), "<p>LeafNode value</p>")

if __name__ == "__main__":
    unittest.main()