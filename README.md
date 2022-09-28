# OpcUaUnitTesting
A Python script that allows a user to connect to a B&R PLC via OpcUa and run unit tests by reading and writing variable values.

## Disclaimer
Changing variable values on the controller for a running machine may lead to unintended consequences. By using this tool, you assume all risks and associated liability. If you use this script on a running machine instead of a simulation, it is critical that you understand exactly what physical components of the machine will be affected. Additionally, it is recommended that you carefully decide which of the PLC's OpcUa nodes should be exposed to the machine network and implement appropriate security measures.

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
Choosing this option will allow you to automatically complete a list of actions related to PLC variables. This option requires you to create a CSV file with the following columns: Action, TaskName, VarName, Input1, Input2. Each line will be a separate action that the script will process in order. When all lines have processed, an output CSV file will be created which will show the result (Success/Fail) of each action as well as provide you with any requested information. Each action can be thought of as a function which takes up to two inputs. For each row Action, TaskName, and VarName must always be filled out with valid information. The available functions are:
- Get: Get the value of a variable. Inputs are ignored. Outputs the value.
- Set: Set the value of a variable. Input1 is the value to set, Input2 is ignored. This action has no Output.
- Wait: Wait before executing the next action. Input1 is the number of seconds to wait, Input2 is ignored. This action has no Output.
- Check: Check the value of a variable against a condition. Input1 is the value to check against, Input2 is the condition. Outputs the result of the check (Valid/Invalid).

**Valid Check Conditions**

When choosing Check as the action for a row, the condition to check with must be entered in input2. The following check conditions are supported:
- '=': Checks that the value of the variable is equal to the check value in input1. If input2 is left blank, the condition is assumed to be '='
- '>': Checks that the value of the variable is greater than the check value in input1.
- '>=': Checks that the value of the variable is greater than or equal to the check value in input1.
- '<': Checks that the value of the variable is less than the check value in input1.
- '<=': Checks that the value of the variable is less than or equal to the check value in input1.
- 'Range' Checks that the variable lies within a range.

If 'Range' is chosen, Input1 must be formatted to show a range. This takes the form of two values (separated by a comma) in between brackets or parentheses. A bracket is inclusive while a parenthesis is exclusive, and they can be mixed. For example:
- [0,30] checks that 0 <= value <= 30
- [1.3, 10.4) checks that 1.3 <= value < 10.4

**Output File**

An output file showing the results of all actions will be generated in the location you provide. This file has five columns: Action, TaskName, VarName, Status, and Output. The Action, TaskName, and VarName columns will exactly match the input file. The Status will show if the action was successful ("Success") or unsuccessful ("Fail"). If the action failed, an error description can be found in the Log (see the [Logging](#logging) section). If the action is successful, the returned output of the action (if one is supplied) will be written in the Output column.

### Disconnect
The Python OpcUa client will disconnect from the PLC server.

## Logging
In most cases, error information will be output to the console. However, the automatic (Import a list of variables) testing will instead output information and errors to a log file named OpcUaUnitTesting_Log.log which will be created in the same directory as the script.

## Automated Testing
In order to test the "Import a list of variables" functionality, there is a test script which can run the main script through custom test cases. All tests are located in the "tests" folder of the repository and the testing script (TestImportFile.py) is located one level up from that. A test case is a folder in the tests directory which contains an input file (Input.csv) and an output file to check against (CorrectOutput.csv). The test script will call the processTestFile function in the main script for each test case and create an Output.csv file in the same folder. It will check Output.csv against CorrectOutput.csv and put any differences in a file called TestOutput.csv. You will get information on the console about which tests have passed and which have failed.

Note that any folders beginning with the ! character will be ignored by the test script. 

There is a batch file in the "tests" folder which will delete all generated output files (Output.csv and TestOutput.csv). This file will permanently delete any files in its folder and any subfolders that match these names exactly.

## Package Dependencies
- csv
- datetime
- opcua
- os
- sys

## Automation Studio Project Dependencies
- Automation Studio version >= 4.12.2.93
- Automation Runtime version B4.93 for ARSim
- mappView version 5.19.0
