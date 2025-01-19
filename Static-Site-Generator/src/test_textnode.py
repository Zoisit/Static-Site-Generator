import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes
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
        delimiter = [(TextType.BOLD, "**"), (TextType.ITALIC, '*'), (TextType.CODE, '`')]
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

        #TODO: add tests for nested
        ## "This is text with a **bolded phrase** in the middle"

    def test_split_nodes_links_and_images(self):
        #base case
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        comp = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, comp)

        #no link
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        comp = [TextNode("", TextType.NORMAL),]
        self.assertEqual(new_nodes, comp)

        new_nodes = split_nodes_link([])
        self.assertEqual(new_nodes, [])

        #link at start and some text at the end
        node = TextNode(
            "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) are links",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        comp = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(" are links", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, comp)

        ##base case images (since same private function is used, other two are omitted)
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        comp = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
        ]
        self.assertEqual(new_nodes, comp)

        #links and images combined
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg). [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) are links instead.",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        comp = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(". ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(" are links instead.", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, comp)
        
    def test_text_to_textnodes(self):
        test = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        comp = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(test), comp)



if __name__ == "__main__":
    unittest.main()