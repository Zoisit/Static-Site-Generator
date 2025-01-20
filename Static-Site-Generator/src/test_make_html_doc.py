import unittest

from make_html_doc import markdown_to_html_node
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_node(self):
        markdown = """# Header

        Paragraph

        - List item 1
        - List item 2

        [link](somewhere)

        ![image](somewhere)

        ### Sub-Header

        *italics*

        **bold**
        """

        html = ParentNode("div", children=[
            ParentNode("h1", [LeafNode(None, "Header")]),
            ParentNode("p", children=[LeafNode(None, value="Paragraph")]),
            ParentNode("ul", children=[ParentNode("li", [LeafNode(None, "List item 1")]), ParentNode("li", [LeafNode(None, "List item 2")])]),
            ParentNode("p", children=[LeafNode("a", "link", props={"href": "somewhere"})]),
            ParentNode("p", children=[LeafNode("img", "", props={"src": "somewhere", "alt": "image"})]),
            ParentNode("h3", [LeafNode(None, "Sub-Header")]),
            ParentNode("p", children=[LeafNode("i", "italics")]),
            ParentNode("p", children=[LeafNode("b", "bold")]),
        ])

        result =  markdown_to_html_node(markdown)
    
        self.assertEqual(html, result)

