from __future__ import annotations

class Node:
    def __init__(self, id:int, parent:Node | None, name:str, children: dict[int, Node] | None = None) -> None:
        self.id = id
        self.parent = parent
        if children is not None:
            self.children = children
        else:
            self.children = {}
        self.name = name
    
    def add_child_node(self, newNode: Node) -> None:
         self.children[newNode.id] = newNode

    def remove_child_node(self, node: Node) -> None:
        self.children.pop(node.id)
