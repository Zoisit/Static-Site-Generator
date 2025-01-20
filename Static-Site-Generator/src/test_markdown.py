import unittest
from markdown import extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type, BlockType


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

    def test_block_to_block_type(self):
        #HEADING = "heading"
        inputs = ["# h1", "## h2", "### h3", "#### h4", "##### h5", "###### h6", "####### to much", "sdf## should not", "###"]
        types = ["heading"] * 6 + ["normal paragraph"] * 3

        for inp, type in zip(inputs, types):
            self.assertEqual(block_to_block_type(inp), type)

        # CODE = "code"
        inputs = ["```some code```", "```not code```text", "text```not code```"]
        types = ["code"] + ["normal paragraph"] * 2
        for inp, type in zip(inputs, types):
            self.assertEqual(block_to_block_type(inp), type)
        
        # QUOTE = "quote"
        inputs = ["> quote", ">quote \n> with\n>\n>4 lines", "not > a quote", "> also \n not \n > a quote"]
        types = ["quote"] * 2 + ["normal paragraph"] * 2
        for inp, type in zip(inputs, types):
            self.assertEqual(block_to_block_type(inp), type)

        # UNORDERED_LIST = "unordered list"
        inputs = ["* line 1", "* line 1\n* line 2\n* line 3", "- line 1", "- line 1\n- line 2\n- line 3", "*line false\n* line 2\n* line 3", "* line 1\n line false\n* line 3", "* line 1\n- line 2"]
        types = ["unordered list"] * 4 + ["normal paragraph"] * 3
        for inp, type in zip(inputs, types):
            self.assertEqual(block_to_block_type(inp), type)
        
        # ORDERED_LIST = "ordered list"
        inputs = ["1. line 1", "1. line 1\n2. line 2\n3. line 3", "0. line 1\n1. line 2\n2. line 3", "1. line false\n* line 2\n3. line 3"]
        types = ["ordered list"] * 2 + ["normal paragraph"] * 2
        for inp, type in zip(inputs, types):
            self.assertEqual(block_to_block_type(inp), type)

        # NORMAL = "normal paragraph" - one in other