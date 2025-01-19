import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()