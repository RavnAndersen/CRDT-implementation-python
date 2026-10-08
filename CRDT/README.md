# CRDT Tree Implementation

A Python implementation of a conflict-free replicated data type (CRDT) for tree structures, based on Martin Kleppmann's paper:  
[*A Highly-Available Move Operation for Replicated Data Trees*](https://martin.kleppmann.com/papers/move-op.pdf).

> **Note:** This algorithm was originally developed for a Year 2 Computer Science group project (an in-home inventory management application). All code in this repository was written solely by me.

---

## Overview

This project implements a replicated tree data structure that automatically resolves concurrent modifications (such as moving, creating, or deleting nodes across multiple devices).

- **Convergence Verified:** Unit tests confirm state convergence when multiple devices interact with the tree and synchronize, all instances converge to the identical state.
- **Test Coverage:** `Unit_tests.py` achieves 92% coverage of `Tree.py`.
- **Limitations:** This is an accurate functional implementation aimed at local simulation and demonstration. It is not optimized for large-scale production use. State synchronization currently uses a local JSON file, though the architecture can be adapted to sync via a remote server or database.

---

## Quick Start & Usage

To simulate multiple devices syncing in real time:
1. Open multiple terminal windows.
2. Run `python main.py` in each terminal.
3. Execute operations across terminals and run `sync` to observe conflict resolution.

### Interacting with the Simulator

| Command | Description |
| :--- | :--- |
| `ls` | Lists all items inside the current directory. |
| `cd <name>` | Moves into a specific folder (e.g., `cd testFolder`). |
| `cd ..` | Moves up one level to the parent directory. |
| `cd /` | Jumps directly to the root directory. |
| `mkdir <name>` | Creates a new folder inside the current directory. |
| `rm <name>` | Deletes a folder and all of its contents. |
| `mv <item_name> <destination>` | Moves a folder to a new location (e.g., another folder or `..`). |
| `sync` | Reprocesses the underlying JSON file to pull remote changes and resolve conflicts. |
| `exit` | Closes the simulator. |

---

## Testing

To run the test suite and verify state convergence:

```bash
pytest Unit_tests.py
