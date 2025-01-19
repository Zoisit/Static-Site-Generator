class HTMLNode():
    def __init__(self, tag:str=None, value:str=None, children:list=None, props:dict=None):
        self.tag:str = tag
        self.value:str = value
        self.children:list = children
        self.props:dict = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        return " " + " ".join(list(map(lambda key: f'{key}="{self.props[key]}"', self.props.keys())))
    
    def __repr__(self):
        return f'HTMLNode(tag={"None" if self.tag == None else f'"{self.tag}"'}, value={"None" if self.value == None else f'"{self.value}"'}, children={"None" if self.children == None else f"{self.children}"}, props={"None" if self.props == None else f"[{self.props_to_html()}]"})' 