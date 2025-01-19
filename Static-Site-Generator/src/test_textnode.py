import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_2(self):
        node = TextNode("", TextType.ITALIC)
        node2 = TextNode("", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_not_eq_3(self):
        node = TextNode("", TextType.LINK)
        node2 = TextNode("", TextType.LINK, url="www.test.de")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.NORMAL, url="www.test.de")
        repr = "TextNode(This is a text node, normal, www.test.de)"
        self.assertEqual(str(node), repr)

    def test_repr_None(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        repr = "TextNode(This is a text node, normal, None)"
        self.assertEqual(str(node), repr)

    def test_text_node_to_html_node(self):
        node = TextNode("test text", None)
        with self.assertRaises(Exception) as context:
            print(text_node_to_html_node(node))
        self.assertTrue("Not a valid TextType" in str(context.exception))

        ## normal text
        node = TextNode("test text", TextType.NORMAL)
        result = LeafNode(None, "test text")
        self.assertEqual(text_node_to_html_node(node), result)
        node = TextNode("test text", TextType.NORMAL, "www.test.url")
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, None)
        self.assertEqual(result.value, "test text")
        self.assertEqual(result.props, None)

        ## BOLD = "bold"
        node = TextNode("test text", TextType.BOLD, "www.test.url")
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, "b")
        self.assertEqual(result.value, "test text")
        self.assertEqual(result.props, None)

        ##ITALIC = "italic"
        node = TextNode("test text", TextType.ITALIC, "www.test.url")
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, "i")
        self.assertEqual(result.value, "test text")
        self.assertEqual(result.props, None)
        
        ##CODE = "code"
        node = TextNode("test text", TextType.CODE, "www.test.url")
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, "code")
        self.assertEqual(result.value, "test text")
        self.assertEqual(result.props, None)
        
        ##LINK = "link"
        node = TextNode("test text", TextType.LINK)
        result = LeafNode("a", "test text", props={"href": None})
        self.assertEqual(text_node_to_html_node(node), result)
        node = TextNode("test text", TextType.LINK, "www.test.url")
        result = LeafNode("a", "test text", props={"href": "www.test.url"})
        self.assertEqual(text_node_to_html_node(node), result)
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, "a")
        self.assertEqual(result.value, "test text")
        self.assertEqual(result.props, {"href": "www.test.url"})
        
        ##IMAGE = "image"
        node = TextNode("test text", TextType.IMAGE, "www.test.url")
        result = LeafNode("img", "", props={"src": "www.test.url", "alt": "test text"})
        self.assertEqual(text_node_to_html_node(node), result)
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, "img")
        self.assertEqual(result.value, "")
        self.assertEqual(result.props, {"src": "www.test.url", "alt": "test text"})
        

if __name__ == "__main__":
    unittest.main()