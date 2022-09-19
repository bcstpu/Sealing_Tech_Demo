# Sealing Tech coding project #
## What does this do? ##
Reads a set of regexes from a config file, applies to a source file, and outputs an output file.
Your regexes must be line separated, so one per line; it uses this to remove "dirty" words from a file.
## Instructions for use ##
By default, the paths as listed in the specifion are fed by command line.
To run, do something like:  **python main.py config.txt source.txt** or, on Ubuntu, **python3 main.py config.txt source.txt** 
## Modifying, default variables, and going beyond spec ##
It is also able to use default arguments, so, running without any command line args will use the default ones.
If you wish to alter the default file paths, and are OK with editing Python, open default_paths.py 
and follow the instructions provided.

