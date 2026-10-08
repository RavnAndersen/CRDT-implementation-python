from Node import Node
from Tree import Tree
import random
import pytest
import json

def _clear_file():
    filename = "sync_devices_file.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump([], file)

def test_add_2_nodes_from_different_ids_concurrently():

    _clear_file()

    root_node_1 = Node(id=0, parent=None, name="root")
    root_node_2 = Node(id=0, parent=None, name="root")
    current_node_1 = root_node_1
    current_node_2 = root_node_2
    crdt_tree_1 = Tree(rootNode=root_node_1, deviceID="startup_load")
    crdt_tree_2 = Tree(rootNode=root_node_2, deviceID="startup_load")

    crdt_tree_1.main_logic()
    crdt_tree_2.main_logic()

    crdt_tree_1.deviceID = 1
    crdt_tree_2.deviceID = 2

    node_1_id = random.randint(10000, 999999)
    node_2_id = random.randint(10000, 999999)

    node_1 = Node(node_1_id, parent=None, name="test1")
    node_2 = Node(node_2_id, parent=None, name="test2")

    crdt_tree_1.add_node(node_1, current_node_1)
    crdt_tree_2.add_node(node_2, current_node_2)

    crdt_tree_1.main_logic()
    crdt_tree_2.main_logic()

    tree_1 = crdt_tree_1.add_tree_to_list(current_node=current_node_1)
    tree_2 = crdt_tree_2.add_tree_to_list(current_node=current_node_2)

    assert tree_1 == ['test1', [], 'test2', []]
    assert tree_2 == ['test1', [], 'test2', []]

    _clear_file()

def test_remove_the_same_node_from_different_ids_concurrently():

    _clear_file()

    root_node_1 = Node(id=0, parent=None, name="root")
    root_node_2 = Node(id=0, parent=None, name="root")
    current_node_1 = root_node_1
    current_node_2 = root_node_2
    crdt_tree_1 = Tree(rootNode=root_node_1, deviceID="startup_load")
    crdt_tree_2 = Tree(rootNode=root_node_2, deviceID="startup_load")

    crdt_tree_1.main_logic()
    crdt_tree_2.main_logic()

    crdt_tree_1.deviceID = 1
    crdt_tree_2.deviceID = 2

    node_1_id = random.randint(10000, 999999)

    node_1 = Node(node_1_id, parent=None, name="test1")

    crdt_tree_1.add_node(node_1, current_node_1)

    crdt_tree_1.main_logic()
    crdt_tree_2.main_logic()

    t1_node1 = crdt_tree_1.treeData[node_1_id]
    crdt_tree_1.remove_node_cascading(t1_node1)

    t2_node1 = crdt_tree_2.treeData[node_1_id]
    crdt_tree_2.remove_node_cascading(t2_node1)

    tree_1 = crdt_tree_1.add_tree_to_list(current_node=current_node_1)
    tree_2 = crdt_tree_2.add_tree_to_list(current_node=current_node_2)

    assert tree_1 == []
    assert tree_2 == []

    _clear_file()

def test_move_node_to_be_child_of_self():

    _clear_file()
    
    root_node = Node(id=0, parent=None, name="root")
    current_node = root_node
    crdt_tree_1 = Tree(rootNode=root_node, deviceID="startup_load")
    crdt_tree_1.main_logic()
    crdt_tree_1.deviceID = 1
    node_1_id = random.randint(10000, 999999)
    node_1 = Node(node_1_id, parent=None, name="test1")

    crdt_tree_1.add_node(node_1, current_node)
    crdt_tree_1.main_logic()
    crdt_tree_1.move_node(node_1, current_node, node_1)
    crdt_tree_1.main_logic()

    tree_1 = crdt_tree_1.add_tree_to_list(current_node=current_node)

    assert tree_1 == ['test1', []]

    _clear_file()

def test_move_2_nodes_to_be_children_of_each_other_from_different_devices_concurrently():

    _clear_file()

    root_node_1 = Node(id=0, parent=None, name="root")
    crdt_tree_1 = Tree(rootNode=root_node_1, deviceID="startup_load")
    
    root_node_2 = Node(id=0, parent=None, name="root")
    crdt_tree_2 = Tree(rootNode=root_node_2, deviceID="startup_load")

    crdt_tree_1.main_logic()
    crdt_tree_2.main_logic()

    crdt_tree_1.deviceID = 1
    crdt_tree_2.deviceID = 2

    node_1_id = random.randint(10000, 999999)
    node_2_id = random.randint(10000, 999999)

    node_1 = Node(node_1_id, parent=None, name="test1")
    node_2 = Node(node_2_id, parent=None, name="test2")

    crdt_tree_1.add_node(node_1, root_node_1)
    crdt_tree_2.add_node(node_2, root_node_2)

    crdt_tree_1.main_logic()
    crdt_tree_2.main_logic()

    t1_node1 = crdt_tree_1.treeData[node_1_id]
    t1_node2 = crdt_tree_1.treeData[node_2_id]
    
    t2_node1 = crdt_tree_2.treeData[node_1_id]
    t2_node2 = crdt_tree_2.treeData[node_2_id]

    crdt_tree_1.move_node(newParent=t1_node1, previousParent=root_node_1, node=t1_node2)
    crdt_tree_2.move_node(newParent=t2_node2, previousParent=root_node_2, node=t2_node1)

    crdt_tree_1.main_logic()
    crdt_tree_2.main_logic()

    tree_1 = crdt_tree_1.add_tree_to_list(current_node=root_node_1)
    tree_2 = crdt_tree_2.add_tree_to_list(current_node=root_node_2)

    assert tree_1 == ['test1', ['test2', []]]
    assert tree_2 == ['test1', ['test2', []]]

    _clear_file()

def test_cascading_deletion_on_node1_and_concurrently_add_node2_to_node1():

    _clear_file()

    root_node_1 = Node(id=0, parent=None, name="root")
    crdt_tree_1 = Tree(rootNode=root_node_1, deviceID="startup_load")
    
    root_node_2 = Node(id=0, parent=None, name="root")
    crdt_tree_2 = Tree(rootNode=root_node_2, deviceID="startup_load")

    crdt_tree_1.main_logic()
    crdt_tree_2.main_logic()

    crdt_tree_1.deviceID = 1
    crdt_tree_2.deviceID = 2

    node_1_id = random.randint(10000, 999999)
    node_2_id = random.randint(10000, 999999)
    node_3_id = random.randint(10000, 999999)

    node_1 = Node(node_1_id, parent=None, name="test1")
    node_2 = Node(node_2_id, parent=None, name="test2")
    node_3 = Node(node_3_id, parent=None, name="control")

    crdt_tree_1.add_node(node_1, root_node_1)
    crdt_tree_1.add_node(node_3, root_node_1)
    crdt_tree_1.main_logic()
    t1_node1 = crdt_tree_1.treeData[node_1_id]
    crdt_tree_1.remove_node_cascading(t1_node1)
    t2_node1 = crdt_tree_1.treeData[node_1_id]
    crdt_tree_2.add_node(node_2, t2_node1)

    crdt_tree_2.main_logic()

    tree_1 = crdt_tree_1.add_tree_to_list(current_node=root_node_1)
    tree_2 = crdt_tree_2.add_tree_to_list(current_node=root_node_2)

    assert tree_1 == ['control', []]
    assert tree_2 == ['control', []]

    _clear_file()

# extra tests

def test_remove_node_promotional():
    _clear_file()
    root = Node(0, None, "Root", None)
    tree = Tree(root, 1)
    
    child = Node(1, None, "Child", None) 
    grandchild = Node(2, None, "Grandchild", None)
    
    tree.add_node(child, root)
    tree.add_node(grandchild, child)
    
    tree.remove_node_promotional(child)
    assert grandchild.parent == root
    assert grandchild.id in root.children
    _clear_file()


def test_undo_redo_missing_parents():
    _clear_file()
    root = Node(0, None, "Root", None)
    tree = Tree(root, 1)
    
    synced_op_missing_parents = {
        "log_time": [2, 2],
        "old_parent": 98,
        "new_parent": 99,
        "log_child": 5,
        "node_name": "RemoteNode"
    }
    
    tree.undo_redo(synced_op_missing_parents)
    assert 98 in tree.treeData
    assert 99 in tree.treeData
    assert tree.treeData[98].name == "Unknown"
    _clear_file()

def test_undo_redo_none_parents():
    _clear_file()
    root = Node(0, None, "Root", None)
    tree = Tree(root, 1)
    
    synced_op_none_parents = {
        "log_time": [3, 2],
        "old_parent": None,
        "new_parent": None,
        "log_child": 6,
        "node_name": "RemoteNodeNoParent"
    }
    
    tree.undo_redo(synced_op_none_parents)
    assert 6 in tree.treeData
    _clear_file()