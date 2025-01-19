from enum import Enum
from leafnode import LeafNode
from markdown import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Not a valid TextType")


## TODO: add processing of nested (recursive)
## TODO: also process non-text nodes         
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        new_strings = old_node.text.split(delimiter)
        if len(new_strings) % 2 == 0:
            raise Exception("Closing delimiter is missing")
        for n in range(len(new_strings)):
            if new_strings[n] == "":
                continue
            if n % 2 == 0:
                new_nodes.append(TextNode(new_strings[n], old_node.text_type))
            else:
                new_nodes.append(TextNode(new_strings[n], text_type))

    return new_nodes

def __split_nodes_markdown(old_nodes, func, text_type, match_prefix=""):
    new_nodes = []
    for old_node in old_nodes:
        remaining_text = old_node.text
        matches = func(remaining_text)

        if len(matches) == 0:
            new_nodes.append(old_node)
            continue

        for match in matches:
            match_text = match_prefix + f"[{match[0]}]({match[1]})"
            new_text = remaining_text.split(match_text, 1)
            if new_text[0].strip() != "":
                new_nodes.append(TextNode(new_text[0], TextType.NORMAL))
            new_nodes.append(TextNode(match[0], text_type, match[1]))
            remaining_text = new_text[1]

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))

    return new_nodes

def split_nodes_image(old_nodes):
    return __split_nodes_markdown(old_nodes, extract_markdown_images, TextType.IMAGE, "!")

def split_nodes_link(old_nodes):
    return __split_nodes_markdown(old_nodes, extract_markdown_links, TextType.LINK)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    delimiter = [(TextType.BOLD, '**'), (TextType.ITALIC, "*"), (TextType.CODE, '`')]
    for t, d in delimiter:
        nodes = split_nodes_delimiter(nodes, d, t)
    return split_nodes_link(split_nodes_image(nodes))

