CRDT algorithm

A python implementation of a CRDT algorithm as outlined by this paper https://martin.kleppmann.com/papers/move-op.pdf 

Please refer to the paper for a description of the algorithm

This algorithm was origionally written for a Year 2 computer science group project, the project was to build an inventory management app for your house. This code is written entirely by me, the other members of the group havent contributed to this.

Run main.py and use this commands to interact with the tree structure.
-----commands------
-------------------
ls: Lists all items inside your current directory.

cd <name>: Moves you into a specific folder (e.g., cd testFolder).

cd ..: Moves you up one level to the parent directory.

cd /: Jumps you to the root directory.

mkdir <name>: Creates a new folder inside your current directory.

rm <name>: Deletes a specific folder and everything inside it.

mv <item_name> <destination>: Moves a folder to a new location. The destination can be another folder name in your current directory, or .. to move it to the parent directory.

sync: Reprocesses the underlying JSON file to pull in any changes made by other terminals and automatically resolves conflicts.   

exit: Shuts down the simulator and closes the terminal.
-------------------