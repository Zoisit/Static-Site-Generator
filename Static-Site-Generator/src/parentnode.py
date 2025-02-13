from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list, props:dict=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent nodes must have a tag")
        if self.children == None:
            raise ValueError("All parent nodes must have a least one child")
        return f"<{self.tag}{self.props_to_html()}>{"".join([c.to_html() for c in self.children])}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"