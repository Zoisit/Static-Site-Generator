import re
from enum import Enum

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def markdown_to_blocks(markdown):
    return list(filter(lambda x: len(x) > 0, ["\n".join([sm.strip() for sm in m.strip().split("\n")]) if "\n" in m.strip() else m.strip() for m in markdown.split("\n\n")]))

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"
    NORMAL = "normal paragraph"

def block_to_block_type(markdown):
    if len(markdown) == 0:
        raise Exception("Markdown should not be empty at this point")
    
    if re.fullmatch(r"(?<!.)#{1,6}(?!#) (.+)", markdown):
        return BlockType.HEADING.value
    if re.fullmatch(r"(?<!.)`{3}(?!#)(.+)`{3}(?!.)", markdown):
        return BlockType.CODE.value
    
    lines = markdown.split("\n")
    if all(l.startswith(">") for l in lines):
        return BlockType.QUOTE.value
    if all(l.startswith("* ") for l in lines) or all(l.startswith("- ") for l in lines):
        return BlockType.UNORDERED_LIST.value
    if all(lines[i][0:3] == f"{i+1}. " for i in range(0, len(lines))):
        return BlockType.ORDERED_LIST.value
    
    return BlockType.NORMAL.value


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.strip().startswith("# "):
            return line.replace("#", "", 1).strip()
    raise Exception("No header (h1) found")