from Node import Node
from Tree import Tree
import random
import pytest
import json

def _clear_file():
    filename = "sync_devices_file.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump([], file)

def test_add_2_nodes_from_different_ids():

    _clear_file()

    root_node = Node(id=0, parent=None, name="root")
    current_node = root_node
    crdt_tree_1 = Tree(rootNode=root_node, deviceID="startup_load")
    crdt_tree_2 = Tree(rootNode=root_node, deviceID="startup_load")

    crdt_tree_1.main_logic()
    crdt_tree_2.main_logic()

    crdt_tree_1.deviceID = 1
    crdt_tree_2.deviceID = 2

    node_1_id = random.randint(10000, 999999)
    node_2_id = random.randint(10000, 999999)

    node_1 = Node(node_1_id, parent=None, name="test1")
    node_2 = Node(node_2_id, parent=None, name="test2")

    crdt_tree_1.add_node(node_1, current_node)
    crdt_tree_2.add_node(node_2, current_node)

    crdt_tree_1.main_logic()
    crdt_tree_2.main_logic()

    tree_1 = crdt_tree_1.add_tree_to_list(current_node=current_node)
    tree_2 = crdt_tree_2.add_tree_to_list(current_node=current_node)

    assert tree_1 == ['test1', [], 'test2', []]
    assert tree_2 == ['test1', [], 'test2', []]

    _clear_file()
