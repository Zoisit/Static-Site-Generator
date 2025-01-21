from textnode import text_to_textnodes, text_node_to_html_node
from markdown import BlockType, markdown_to_blocks, block_to_block_type
from parentnode import ParentNode

def __get_block_values(markdown, delimiter_size):
    return [line[delimiter_size:] for line in markdown.split("\n")]

def __get_children(content):
    return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(content)]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    nodes = []
    for block in blocks:
        bt = block_to_block_type(block)

        match bt:
            case BlockType.HEADING.value:
                block_split = block.split(" ", 1)
                heading_type = block_split[0].count("#")
                test = ParentNode(f"h{heading_type}", children=__get_children(block_split[1]))
                nodes.append(test)
            case BlockType.CODE.value:
                content = block[3:-3]
                nodes.append(ParentNode("pre", "", [ParentNode("code", __get_children(content))]))
            case BlockType.QUOTE.value:
                content = " ".join(__get_block_values(block, 1)).strip()
                nodes.append(ParentNode("blockquote", __get_children(content)))
            case BlockType.UNORDERED_LIST.value:
                content = __get_block_values(block, 2)
                inner_html = [ParentNode("li", __get_children(line)) for line in content]
                nodes.append(ParentNode("ul", children=inner_html))
            case BlockType.ORDERED_LIST.value:
                content = __get_block_values(block, 3)
                inner_html = [ParentNode("li", __get_children(line)) for line in content]
                nodes.append(ParentNode("ol", children=inner_html))
            case BlockType.NORMAL.value:
                textnodes = text_to_textnodes(block)
                nodes.append(ParentNode("p", children=[text_node_to_html_node(tn) for tn in textnodes]))

    return ParentNode("div", children=nodes)

