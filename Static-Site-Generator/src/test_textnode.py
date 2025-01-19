import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter
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
        
    def test_split_nodes_delimiter(self):
        ## exception
        node = TextNode("This is text with a `code block word", TextType.NORMAL)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertTrue("Closing delimiter is missing" in str(context.exception))
        
        node = TextNode("This is text with one `code block word and another `code block` word", TextType.NORMAL)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertTrue("Closing delimiter is missing" in str(context.exception))
        
        ## base case
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, result)

        ## don't touch non-normal text
        node = TextNode("*This is bold text with a `code block` word and another `code block` word*", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("*This is bold text with a `code block` word and another `code block` word*", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, result)

        ## test different delimiters
        delimiter = [(TextType.BOLD, "*"), (TextType.ITALIC, '**'), (TextType.CODE, '`')]
        for t, d in delimiter:
            node = TextNode(f"This is text with a {d}delimiter block{d} word and another {d}delimiter block{d} word", TextType.NORMAL)
            new_nodes = split_nodes_delimiter([node], "`", t)
            result = [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("delimiter block", t),
                TextNode(" word and another ", TextType.NORMAL),
                TextNode("delimiter block", t),
                TextNode(" word", TextType.NORMAL),
            ]
        self.assertEqual(new_nodes, result)
        
        ## test similar delimiters
        node = TextNode("**bold** and *italic*", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

        ##TODO: process non-text nodes

        #TODO: add tests for nested
        ## "This is text with a **bolded phrase** in the middle"

if __name__ == "__main__":
    unittest.main()