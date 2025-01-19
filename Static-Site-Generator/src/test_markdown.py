import unittest
from markdown import extract_markdown_images, extract_markdown_links, markdown_to_blocks


class TestMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

        text = "This is text with a link, not images, [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_images(text), [])
 


    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
 
        text = "This is a wrong text with no working markdown link [to boot dev(https://www.boot.dev) and to youtube]"
        self.assertEqual(extract_markdown_links(text), [])
 
    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        


        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""


        exp = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", """* This is the first list item in a list block
        * This is a list item
        * This is another list item"""]

        self.assertEqual(markdown_to_blocks(markdown), exp)