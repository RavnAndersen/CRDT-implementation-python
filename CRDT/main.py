from Node import Node
from Tree import Tree
import random

def get_destination_node(current: Node, root: Node, path: str) -> Node | None:
    """Helper function to resolve simple paths for moving nodes."""
    if path == "/":
        return root
    if path == "..":
        return current.parent if current.parent else current
    # Search for a child folder in the current directory
    for child in current.children.values():
        if child.name == path:
            return child
    return None

def run_cli() -> None:
    print("=== CRDT File System Simulator ===")
    user_input = input("Enter a unique Device ID (integer) for this terminal: ")
    device_id = int(user_input) if user_input.isdigit() else 1

    # Initialize the root Node[cite: 1] and the Tree
    root_node = Node(id=0, parent=None, name="root")
    crdt_tree = Tree(rootNode=root_node, deviceID=device_id)
    
    print("Syncing with network...")
    crdt_tree.deviceID = "startup_load"
    crdt_tree.main_logic() # Process existing operations from the JSON file[cite: 4]
    crdt_tree.deviceID = device_id
    
    current_node = root_node
    
    while True:
        command_line = input(f"/{current_node.name}> ").strip().split()
        if not command_line:
            continue
            
        command = command_line[0].lower()
        args = command_line[1:]
        
        # --- NAVIGATION ---
        if command == "exit":
            break
            
        elif command == "ls":
            if not current_node.children:
                print(" (empty)")
            else:
                for child in current_node.children.values():
                    print(f" - {child.name} [ID: {child.id}]")
                    
        elif command == "cd":
            if not args:
                continue
            target = args[0]
            if target == "..":
                if current_node.parent is not None:
                    current_node = current_node.parent
            elif target == "/":
                current_node = root_node
            else:
                found = False
                for child in current_node.children.values():
                    if child.name == target:
                        current_node = child
                        found = True
                        break
                if not found:
                    print(f"Directory '{target}' not found.")
                    
        # --- CRDT OPERATIONS ---
        elif command == "mkdir":
            if not args:
                print("Usage: mkdir <name>")
                continue
            name = args[0]
            # Generate a random ID to prevent collisions across different terminals
            new_id = random.randint(10000, 999999)
            # Create a new Node passing id, parent, and name[cite: 1]
            new_node = Node(id=new_id, parent=current_node, name=name)
            # Add the new node to the tree via wrapper function[cite: 4]
            crdt_tree.add_node(new_node, current_node)
            print(f"Created '{name}'.")
            
        elif command == "rm":
            if not args:
                print("Usage: rm <name>")
                continue
            target = args[0]
            target_node = None
            for child in current_node.children.values():
                if child.name == target:
                    target_node = child
                    break
            
            if target_node:
                # Remove the node from the parent's list of children using the cascading wrapper[cite: 4]
                crdt_tree.remove_node_cascading(target_node)
                print(f"Removed '{target}'.")
            else:
                print(f"'{target}' not found.")
                
        elif command == "mv":
            if len(args) < 2:
                print("Usage: mv <item_name> <destination_name_or_..>")
                continue
            target_name = args[0]
            dest_name = args[1]
            
            # 1. Find the node you want to move
            node_to_move = None
            for child in current_node.children.values():
                if child.name == target_name:
                    node_to_move = child
                    break
                    
            if not node_to_move:
                print(f"'{target_name}' not found.")
                continue
                
            # 2. Find the destination node
            new_parent = get_destination_node(current_node, root_node, dest_name)
            if not new_parent:
                print(f"Destination '{dest_name}' not found.")
                continue
                
            # Move the node using the wrapper function which handles previousParent and newParent[cite: 4]
            crdt_tree.move_node(newParent=new_parent, previousParent=current_node, node=node_to_move)
            print(f"Moved '{target_name}' to '{new_parent.name}'.")
            
        elif command == "sync":
            # Reprocess the JSON file to fetch remote operations and run undo_redo logic[cite: 4]
            crdt_tree.main_logic()
            # If the current node was deleted by someone else, jump back to root to prevent crashing
            if current_node.id not in crdt_tree.treeData and current_node.id != 0:
                print("Your current directory was deleted remotely. Returning to root.")
                current_node = root_node
            print("Synced with network. Type 'ls' to see changes.")
            
        else:
            print(f"Unknown command: {command}. (Available: ls, cd, mkdir, rm, mv, sync, exit)")

if __name__ == "__main__":
    run_cli()