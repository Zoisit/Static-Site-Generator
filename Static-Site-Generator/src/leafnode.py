from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag:str, value:str, props:dict=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"