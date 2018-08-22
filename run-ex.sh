#!/bin/bash

# This file is an example bash executable that allows you to 
# run individual shell commands in batch mode. Using these bash
# scripts are also a convenient way to record (remember) complex
# run commands. 
#
# To run the this bash script: 
# $ . run-ex.sh
# or
# source run-example.sh
#
# To create a run script you have to do the following
# - create a new file and add #!/bin/bash to the first line
#   (This tells the computer that it is reading a bash script)
# - add the lines of code that you want to have executed. 
#   Usually this would be the commands you use at the command 
#   prompt. If you have multiple lines, they will be executed
#   sequentially
# - save the file with the .sh extension
# - run the following command:
#   $ chmod +x filename.sh      
#   where filename.sh is the file you saved in the previous step.
#   This command turns the filename.sh into an executable and
#   if you run $ ls - l you will see that x has been added to 
#   the file permissions.  
# - run your bash script using $ . filename.sh
#
# Authors: Ingo Jahn
# Last modified: 2018/08/13


# e4shared --custom-post --script-file="example-1.lua"
# e4shared --custom-post --script-file="example-2.lua"

# e4shared --custom-post --script-file="path-example-1.lua"
# e4shared --custom-post --script-file="path-example-2.lua"
# e4shared --custom-post --script-file="path-example-3.lua"
# e4shared --custom-post --script-file="path-example-4.lua"
# e4shared --custom-post --script-file="path-example-5.lua"

e4shared --custom-post --script-file="surface.lua"
#foamMesh --job=surface --verbosity=2


# e4shared --custom-post --script-file="surface-example-2.lua"
# e4shared --custom-post --script-file="surface-example-3.lua"

# e4shared --custom-post --script-file="volume-example-1.lua"
# e4shared --custom-post --script-file="volume-example-2.lua"
# e4shared --custom-post --script-file="volume-example-3.lua"
