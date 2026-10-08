# CRDT Tree Implementation

A Python implementation of a conflict-free replicated data type (CRDT) for tree structures, based on Martin Kleppmann's paper:  
[*A Highly-Available Move Operation for Replicated Data Trees*](https://martin.kleppmann.com/papers/move-op.pdf)[cite: 1].

> **Note:** This algorithm was originally developed for a Year 2 Computer Science group project (an in-home inventory management application)[cite: 1]. All code in this repository was written solely by me[cite: 1].

---

## Overview

This project implements a replicated tree data structure that automatically resolves concurrent modifications (such as moving, creating, or deleting nodes across multiple devices)[cite: 1].

- **Convergence Verified:** Unit tests confirm state convergence—when multiple devices interact with the tree and synchronize, all instances converge to the identical state[cite: 1].
- **Test Coverage:** `Unit_tests.py` achieves 92% coverage of `Tree.py`[cite: 1].
- **Limitations:** This is an accurate functional implementation aimed at local simulation and demonstration[cite: 1]. It is not optimized for large-scale production use[cite: 1]. State synchronization currently uses a local JSON file, though the architecture can be adapted to sync via a remote server or database[cite: 1].

---

## Quick Start & Usage

To simulate multiple devices syncing in real time:
1. Open multiple terminal windows[cite: 1].
2. Run `python main.py` in each terminal[cite: 1].
3. Execute operations across terminals and run `sync` to observe conflict resolution[cite: 1].

### Interacting with the Simulator

| Command | Description |
| :--- | :--- |
| `ls` | Lists all items inside the current directory[cite: 1]. |
| `cd <name>` | Moves into a specific folder (e.g., `cd testFolder`)[cite: 1]. |
| `cd ..` | Moves up one level to the parent directory[cite: 1]. |
| `cd /` | Jumps directly to the root directory[cite: 1]. |
| `mkdir <name>` | Creates a new folder inside the current directory[cite: 1]. |
| `rm <name>` | Deletes a folder and all of its contents[cite: 1]. |
| `mv <item_name> <destination>` | Moves a folder to a new location (e.g., another folder or `..`)[cite: 1]. |
| `sync` | Reprocesses the underlying JSON file to pull remote changes and resolve conflicts[cite: 1]. |
| `exit` | Closes the simulator[cite: 1]. |

---

## Testing

To run the test suite and verify state convergence:

```bash
pytest Unit_tests.py