from Node import Node
import json
from typing import Any

class Tree:
    def __init__(self, rootNode:Node, deviceID:int, syncFilePath = "sync_devices_file.json") -> None:
        self.rootNode = rootNode
        self.treeData = {rootNode.id:rootNode}
        self.discardNode = Node(1, None, "DISCARD", None)
        self.treeData[self.discardNode.id] = self.discardNode
        self.syncFilePath = syncFilePath

        # undo redo
        self.deviceID = deviceID
        self.clock = 0
        self.seenOperations = set()
        self.log = []
    
    # Wrapper functions ------------------------------------------------------
    def add_node(self, newNode:Node, parentNode:Node) -> None:
         self.clock += 1
         new_timeStamp = (self.clock, self.deviceID)
         self.do_operation(new_timeStamp, None, parentNode, newNode, True)
         self.treeData[newNode.id] = newNode
         

    def remove_node_cascading(self, node:Node) -> None:
        if node.parent is not None: # root node doesnt have a parent
            # remove the node from the parents list of children
            self.clock += 1
            new_timeStamp = (self.clock, self.deviceID)
            self.do_operation(new_timeStamp, node.parent, self.discardNode, node, True)

    def remove_node_promotional(self, node:Node) -> None:
        if node.parent is not None: # root node doesnt have a parent
            for child in node.children.values():
                self.add_node(child,node.parent) # add the children to the children of the parent
                child.parent = node.parent
            # remove the node from the parents list of children
            self.clock += 1
            new_timeStamp = (self.clock, self.deviceID)
            self.do_operation(new_timeStamp, node.parent, self.discardNode, node, True)
        else:
            raise Exception("Cannot delete root node in a promotional way")
        
    def move_node(self, newParent:Node, previousParent:Node, node:Node) -> None:
        self.clock += 1
        new_timeStamp = (self.clock, self.deviceID)
        self.do_operation(new_timeStamp, previousParent, newParent, node, True)
    # Wrapper functions ------------------------------------------------------

    # The base function for every operation done to the Tree
    def do_operation(self, new_timeStamp:tuple[int,int], previousParent:Node | None, newParent:Node | None, node:Node, localFlag:bool) -> None:

        # create the log entry
        log_entry = {
            "log_time": new_timeStamp,
            "old_parent": previousParent.id if previousParent else None,
            "new_parent": newParent.id,
            "log_child": node.id,
            "node_name": node.name
        }

        # add the log entry to the front of the local list
        self.log.insert(0, log_entry)

        # if the operation was local then it needs to be added to the sync file
        if localFlag:
            self.log_operation(self.syncFilePath, log_entry)

        # check if Node is newParent or an ancestor of new parent
        # you cannot move a child to be the parent or child of itself
        def _cycle_check(newParent:Node, node:Node):
            if newParent is None:
                return False
            if newParent.id == node.id:
                return True
            return _cycle_check(newParent.parent, node)
        
        if not _cycle_check(newParent, node):
            # Remove the node from its current parent before moving it
            if node.parent is not None:
                node.parent.remove_child_node(node)
            
            # Apply to the new parent 
            newParent.add_child_node(node)
            node.parent = newParent

    # the function that adds a log to the file
    def log_operation(self, filePath:str, log_entry:dict[str, Any]) -> None:
        try:
            # load the sync file
            with open(filePath,"r") as fRead:
                listObj = json.load(fRead)
        except (FileNotFoundError, json.JSONDecodeError):
            listObj = []
        
        # add the new log to the json object
        listObj.append(log_entry)
        # update the file
        with open(filePath, 'w') as fWrite:
                json.dump(listObj, fWrite, indent=4, separators=(',',': '))
            
    # undoes operations which are newer than one that you just found, and then redoes them in the right order
    def undo_redo(self, syncedOperation:dict[str, Any]) -> None:
        # Makes sure it doesnt crash before loading operations into the program
        if syncedOperation["log_child"] not in self.treeData:
            self.treeData[syncedOperation["log_child"]] = Node(syncedOperation["log_child"], None, syncedOperation["node_name"], None)

        # ----------------------------------------------------------------------------------------------------------
        # Undo all operations until you get to a log_time which is older then the newly introduced operation
        # When you arrive at this point you can do this newly introduced operation and then redo the rest of the undid operations
        # ----------------------------------------------------------------------------------------------------------
        tempUndone = []
        if self.log:
            while len(self.log) and self.log[0]["log_time"] > tuple(syncedOperation["log_time"]):
                poppedOperation = self.log.pop(0)
                tempUndone.insert(0, poppedOperation)
                self._undo(poppedOperation)
        # ----------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------
        # do the newly introduced operation
        # --------------------------------------------------------------------------------------------------------
        new_timeStampFirst = tuple(syncedOperation["log_time"])
        if syncedOperation["new_parent"] is not None:
            if syncedOperation["new_parent"] not in self.treeData:
                self.treeData[syncedOperation["new_parent"]] = Node(id=syncedOperation["new_parent"], parent=None, name="Unknown")
            newParentFirst:Node = self.treeData[syncedOperation["new_parent"]]
        else:
            newParentFirst = None

        if syncedOperation["old_parent"] is not None:
            if syncedOperation["old_parent"] not in self.treeData:
                self.treeData[syncedOperation["old_parent"]] = Node(id=syncedOperation["old_parent"], parent=None, name="Unknown")
            previousParentFirst:Node = self.treeData[syncedOperation["old_parent"]]
        else:
            previousParentFirst = None
    
        nodeFirst:Node = self.treeData[syncedOperation["log_child"]]
        localFlagFirst = False
        self.do_operation(new_timeStampFirst, previousParentFirst, newParentFirst, nodeFirst, localFlagFirst)
        # --------------------------------------------------------------------------------------------------------

        # redo every other operation
        for operation in tempUndone:

            new_timeStamp = operation["log_time"]
            if operation["new_parent"] is not None:
                newParent:Node = self.treeData[operation["new_parent"]]
            else:
                newParent = None
    
            if operation["old_parent"] is not None:
                previousParent:Node = self.treeData[operation["old_parent"]]
            else:
                previousParent = None

            node:Node = self.treeData[operation["log_child"]]
            localFlag = False

            self.do_operation(new_timeStamp, previousParent, newParent, node, localFlag)
        

    # undoes an operation passed into it
    def _undo(self, operation:dict[str, Any]) -> None:

        if operation["new_parent"] is not None:
            newParent:Node = self.treeData[operation["new_parent"]]
        else:
            newParent = None
    
        if operation["old_parent"] is not None:
            previousParent:Node = self.treeData[operation["old_parent"]]
        else:
            previousParent = None
    
        node:Node = self.treeData[operation["log_child"]]

        if newParent is not None and node.parent == newParent:
            newParent.remove_child_node(node)
            if previousParent is not None:
                previousParent.add_child_node(node)
            node.parent = previousParent
        
    def main_logic(self) -> None:
        try:
            with open(self.syncFilePath, "r") as f:
                allOperations = json.load(f)
        except(FileNotFoundError, json.JSONDecodeError):
            allOperations = []
        
        for operations in allOperations:
            timeStamp = tuple(operations["log_time"])

            if timeStamp not in self.seenOperations:
                if timeStamp[1] != self.deviceID:
                    self.clock = max(timeStamp[0],self.clock)
                    self.undo_redo(operations)
                self.seenOperations.add(timeStamp)