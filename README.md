# OpcUaUnitTesting
A package that allows a user to connect to a B&R PLC via OpcUa and run unit tests

## How to Use
After starting the OpcUaUnitTesting script, you will be prompted to input the IP address of the server PLC and the port on which the server is hosting OpcUa communication. Optionally, you can also enter a username. If one is entered, you will then be prompted for a password. This allows you to connect either anonymously or with login credentials, depending on what the server supports.

You will then be presented with a list of options:
- A: Get a list of PLC tasks 
- B: Get a list of PLC variables by task
- C: Get the value of a specific PLC variable
- D: Set the value of a specific PLC variable
- E: Import a list of variables
- Z: Disconnect

Choose an option by entering the letter corresponding with your choice (case-insensitive)

## Features
### Get a list of PLC tasks
The script will browse the server and return a list of task nodes. Note that this will not show all tasks running on the PLC, just the ones that have exposed OpcUa variables. If any global variables are available, AsGlobalPV will be at the top of the list. Note that this is not a PLC task but the namespace for Automation Runtime global variables

### Get a list of PLC variables by task
The script will first show all available PLC tasks as with option A in a numbered list. You can choose the number of the task you want to view, and the script will return all OpcUa nodes associated with that task. The information returned will only include the variable names.

### Get the value of a specific PLC variable
Choosing this option will prompt you to enter the name of a task and a variable within that task. Then, the current value of that variable will be printed to the console. You must enter the names exactly as they exist in the OpcUa namespace. For example, if a task name is truncated in the Software configuration, that truncated name must be entered into the terminal. If you are unsure of the name of a variable or task, the two previous options should help you.

### Set the value of a specific PLC variable
Choosing this option will prompt you to enter the name of a task and a variable within that task, as well as a value to set the variable with. The value you enter will be converted to match the variable's datatype and then the variable will be set. You must enter the names exactly as they exist in the OpcUa namespace. For example, if a task name is truncated in the Software configuration, that truncated name must be entered into the terminal. If you are unsure of the name of a variable or task, the two previous options should help you.

### Import a list of variables
ToDo

### Disconnect
The Python OpcUa client will disconnect from the PLC server.

## Package Dependencies
- csv
- datetime
- opcua
- os
- sys
