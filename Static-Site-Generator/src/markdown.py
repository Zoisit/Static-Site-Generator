import re

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def markdown_to_blocks(markdown):
    return list(filter(lambda x: len(x) > 0, [m.strip() for m in markdown.split("\n\n")]))
