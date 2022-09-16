"""
OpcUaUnitTesting main script

Marcus Mangel <marcus.mangel@br-automation.com>

"""

######## Import Libraries ########

import sys
import os
from os.path import exists
import logging
from opcua import Client, ua, Node
from datetime import datetime
import csv

######## Structure Declarations ########
# ConfigDef class is used for input configuration files
# Each line of the input file is an instance of this class
class ConfigDef:
    def __init__(self, action, taskName, varName, input1, input2):
        self.action = action
        self.taskName = taskName
        self.varName = varName
        self.input1 = input1
        self.input2 = input2

    def __repr__(self):
        return repr((self.action, self.taskName, self.varName, self.input1, self.input2))

# ResultDef class is used for output result files
# Each line of the output file is an instance of this class
class ResultDef:
    def __init__(self, action, taskName, varName):
        self.action = action
        self.taskName = taskName
        self.varName = varName
        self.status = "Initialized"
        self.output = " "

    def __repr__(self):
        return repr((self.action, self.taskName, self.varName, self.status, self.output))

######## Constant Variables ########

BNR_TASKS_PATH = "ns=6;s=::"

######## Declare Functions ########

# Function which prints a List to the console
# Each item is preceded by its Index in the List
# Requires: A variable of List type
# Modifies: Only local variables
# Returns: Nothing
def printList(List):
    ListIndex = 0
    while ListIndex < len(List):
        print(ListIndex, ":", List[ListIndex])
        ListIndex += 1

# Function which seaches the client for PLC tasks at the expected namespace
# creates a list of tasks and prints that list
# Requires: An OpcUa Client
# Modifies: Only local variables
# Returns: A List of Nodes found on the Client that correspond to PLC tasks
def getPLCTasks(client):
    ServerTasksRootNode = client.get_node(BNR_TASKS_PATH)
    ListOfTaskNodes = ServerTasksRootNode.get_children()
    return ListOfTaskNodes

# Function which displays the list of tasks found on the PLC
# and lets a user choose a task, then displays all found tags
# related to that task
# Requires: An OpcUa Client
# Modifies: Only local variables
# Returns: A List of OpcUa nodes found on the Client
def getPLCTags(client):
    # Get and display list of PLC tasks
    try:
        ListOfTaskNodes = getPLCTasks(client)
    except Exception as exc:
        print('\n',exc)
        raise Exception("Failed to get list of PLC tasks!")
    else:
        ListOfTaskNames = []
        for Task in ListOfTaskNodes:
            TaskName = Task.get_browse_name()
            ListOfTaskNames.append(TaskName.Name)
        print("Tasks found:\n")
        printList(ListOfTaskNames)
    # User chooses a task
    TaskToSearch = input("Input the number of the task to examine: ")
    # Find variables that live within the given task
    ListOfPVNodes = ListOfTaskNodes[int(TaskToSearch)].get_children()
    return ListOfPVNodes

# Function which converts user input (string) to a valid datatype variant
# Requires: The input datatype (inputStr) and the Variant Type required (variantType)
# Modifies: Only local variables
# Returns The converted value
def convertOpcUaType(inputStr, variantType):
    value = "Not converted yet"
    if variantType == ua.VariantType.String:
        try:
            value = inputStr
        except:
            raise ValueError("Invalid input. PLC variable is String")
            return 0
    elif variantType == ua.VariantType.Boolean:
        try:
            value = int(inputStr)
        except:
            raise ValueError("Invalid input. PLC variable is Boolean")
            return 0
    elif variantType == ua.VariantType.SByte:
        try:
            value = int(inputStr)
        except:
            raise ValueError("Invalid input. PLC variable is SByte")
            return 0
    elif variantType == ua.VariantType.Byte:
        try:
            value = int(inputStr)
        except:
            raise ValueError("Invalid input. PLC variable is Byte")
            return 0
    elif variantType == ua.VariantType.Int16:
        try:
            value = int(inputStr)
        except:
            raise ValueError("Invalid input. PLC variable is Int16")
            return 0
    elif variantType == ua.VariantType.UInt16:
        try:
            value = int(inputStr)
        except:
            raise ValueError("Invalid input. PLC variable is UInt16")
            return 0
    elif variantType == ua.VariantType.Int32:
        try:
            value = int(inputStr)
        except:
            raise ValueError("Invalid input. PLC variable is Int32")
            return 0
    elif variantType == ua.VariantType.UInt32:
        try:
            value = int(inputStr)
        except:
            raise ValueError("Invalid input. PLC variable is UInt32")
            return 0
    elif variantType == ua.VariantType.Int64:
        try:
            value = int(inputStr)
        except:
            raise ValueError("Invalid input. PLC variable is Int64")
            return 0
    elif variantType == ua.VariantType.UInt64:
        try:
            value = int(inputStr)
        except:
            raise ValueError("Invalid input. PLC variable is UInt64")
            return 0
    elif variantType == ua.VariantType.Float:
        try:
            value = float(inputStr)
        except:
            raise ValueError("Invalid input. PLC variable is Float")
            return 0
    elif variantType == ua.VariantType.Double:
        try:
            value = float(inputStr)
        except:
            raise ValueError("Invalid input. PLC variable is Double")
            return 0
    elif variantType == ua.VariantType.DateTime:
        try:
            value = datetime.strptime(inputStr, '%Y-%m-%d %H:%M:%S')
        except ValueError as ve:
            print('\n',ve)
            raise ValueError("Invalid input. PLC variable is DateTime")
            return 0
        except:
            raise ValueError("Invalid input. PLC variable is DateTime")
            return 0
    return value

# Gets the value of a variable on the PLC
# Requires An OpcUa Client, the name of a Task and the name of a Variable in that task
# Modifies: Only local variables
# Returns the value using OpcUa Client get_value() function
def getValueOfNode(client, taskName, varName):
    # Find the requested node on the server
    nodeName = BNR_TASKS_PATH + taskName + ":" + varName
    try:
        node = client.get_node(nodeName)
    except Exception as exc:
        print('\n',Exc)
        raise RuntimeError()
        return 0
    # Get the Node's value
    try:
        value = node.get_value()
    except Exception as exc:
        print('\n',exc)
        raise RuntimeError()
        return 0
    else:
        return value

# Sets the value of a variable on the PLC
# Requires An OpcUa Client, the name of a Task,
# the name of a Variable in that task, and a Value to set
# Modifies: The value of the OpcUa Node on the remote client
# Returns: Nothing
def setValueOfNode(client, taskName, varName, value):
    # Find the requested node on the server
    nodeName = BNR_TASKS_PATH + taskName + ":" + varName
    try:
        node = client.get_node(nodeName)
    except Exception as exc:
        print('\n',exc)
        raise RuntimeError()
        return
    # Get the datatype of the node on the server
    variantType = node.get_data_type_as_variant_type()
    # User input must be cast to match server variable type
    try:
        value = convertOpcUaType(value,variantType)
    except ValueError as ve:
        print(ve)
        raise ValueError()
        return
    # Set the variable's value
    try:
        node.set_value(ua.DataValue(ua.Variant(value, variantType)))
    except Exception as exc:
        print('\n',exc)
        raise RuntimeError()
    return

# Checks the value of a variable on the PLC against a condition
# Supported conditions: =, <, >, <=, >=
# Requires An OpcUa Client, the name of a Task and the name of a Variable in that task,
# a value to check against, and a condition with which to do the check
# Modifies: Only local variables
# Returns the result of the check as a boolean
def checkValueOfNode(client, taskName, varName, checkValue, condition):
    # Get the value of the node on the server
    value = getValueOfNode(client,taskName,varName)
    # Get the datatype of the node on the server
    nodeName = BNR_TASKS_PATH + taskName + ":" + varName
    node = client.get_node(nodeName)
    variantType = node.get_data_type_as_variant_type()
    # Convert the checkValue to the correct datatype
    checkValue = convertOpcUaType(checkValue,variantType)

    # Perform the check
    if condition == '=':
        if value == checkValue:
            return True
        else:
            return False
    elif condition == '>':
        if value > checkValue:
            return True
        else:
            return False
    elif condition == '<':
        if value < checkValue:
            return True
        else:
            return False
    elif condition == '>=':
        if value >= checkValue:
            return True
        else:
            return False
    elif condition == '<=':
        if value <= checkValue:
            return True
        else:
            return False
    else:
        print("Invalid condition")
        return False

# Function which imports a CSV test config file
# Expected format is "Variable name,value,time(s)"
# For example: "AsGlobalPV:TestUSINT,50,10"
# Requires: A valid file path
# Modifies: Only local variables
# Returns: A list of configuration defintions of ConfigDef datatype
def importTestFile(filename):
    configDefList = []
    with open(filename, mode='r', encoding='utf-8-sig') as csvFile:
        csvReader = csv.DictReader(csvFile)
        lineCount = 0
        for row in csvReader:
            configDefList.append(ConfigDef(row["Action"],row["TaskName"],row["VarName"],row["Input1"],row["Input2"]))
            lineCount += 1
        print(f'\nRead {lineCount} lines in from CSV file')
    return configDefList

# Function which exports a CSV test results file
# Requires: A list of ResultDef types and a valid file path for the CSV file
# Modifies: The output file
# Returns: Nothing
def exportValuesToTestFile(ListOfVars, filename):
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as csvFile:
        fieldnames = ['Action','TaskName','VarName','Status','Output']
        csvWriter = csv.DictWriter(csvFile, fieldnames = fieldnames)
        csvWriter.writeheader()
        lineCount = 0
        for var in ListOfVars:
            csvWriter.writerow({'Action':var.action,'TaskName':var.taskName,'VarName':var.varName,'Status':var.status,'Output':var.output})
            lineCount += 1
        print(f'\nWrote {lineCount} lines to Output CSV file')
    return

# Function which processes an entry line in an import file
# Requires: An OpcUa client, an input file line to process
# Modifies: Only local variables
# Returns: An entry to be added to the output file
def processTestFileEntry(client, CurrentVar):
    OutputEntry = ResultDef(CurrentVar.action,CurrentVar.taskName,CurrentVar.varName)
    if (CurrentVar.action == 'Get'):
        logging.info('Getting %s',CurrentVar.varName)
        try:
            Value = getValueOfNode(client, CurrentVar.taskName, CurrentVar.varName)
        except:
            logging.warning('Get Value failed!')
            OutputEntry.status = 'Fail'
        else:
            logging.info('The value of the chosen variable is: %s', str(Value))
            OutputEntry.status = 'Success'
            OutputEntry.output = Value
    elif (CurrentVar.action == 'Set'):
        logging.info('Setting %s to %s', CurrentVar.varName, CurrentVar.input1)
        try:
            setValueOfNode(client, CurrentVar.taskName, CurrentVar.varName, CurrentVar.input1)
        except ValueError as ve:
            logging.warning('Variable was not set! %s', ve)
            OutputEntry.status = 'Fail'
        except RuntimeError as re:
            logging.warning('Variable was not set! %s', re)
            OutputEntry.status = 'Fail'
        except:
            logging.warning('Variable was not set!')
            OutputEntry.status = 'Fail'
        else:
            logging.info('Variable set successfully')
            OutputEntry.status = 'Success'
    elif (CurrentVar.action == 'Check'):
        logging.info('Checking %s', CurrentVar.varName)
        try:
            checkResult = checkValueOfNode(client, CurrentVar.taskName, CurrentVar.varName, CurrentVar.input1, CurrentVar.input2)
        except Exception as exc:
            logging.warning('Check Value failed! %s', exc)
            OutputEntry.status = 'Fail'
        else:
            OutputEntry.status = 'Success'
            logging.info('Check value completed successfully')
            if checkResult:
                OutputEntry.output = 'Valid'
            else:
                OutputEntry.output = 'Invalid'
    elif (CurrentVar.action == 'Wait'):
        print('Waiting for', CurrentVar.input1, 'seconds')
        startTime = datetime.now()
        timeElapsedInSeconds = 0
        timeToWait = int(CurrentVar.input1)
        while (timeElapsedInSeconds < timeToWait):
            currentTime = datetime.now()
            timeElapsed = currentTime - startTime
            timeElapsedInSeconds = timeElapsed.total_seconds()
        OutputEntry.status = 'Success'
    else:
        logging.warning("Invalid action requested")
    return OutputEntry

# Function which shows the user a menu and processes responses
# Requires: An OpcUa Client
# Modifies: Only local variables
# Returns: Nothing
def menu(client):
    # Display menu and wait for input
    print("\nWelcome to the OpcUa Unit Tester! Please enter the letter corresponding to the desired option: ")
    print("A. Get a list of PLC tasks")
    print("B. Get a list of PLC variables by task")
    print("C. Get the value of a specific PLC variable")
    print("D. Set the value of a specific PLC variable")
    print("E. Import a list of variables")
    print("Z. Disconnect")
    optionChoice = input()
    endMenu = False

    # Perform action based on chosen option
    if optionChoice == "A" or optionChoice == "a": # Get list of tasks as nodes
        try:
            ListOfTaskNodes = getPLCTasks(client)
        except Exception as exc:
            print('\n', exc)
            print("Get tasks failed!")
        else:
            ListOfTaskNames = []
            for Task in ListOfTaskNodes:
                TaskName = Task.get_browse_name()
                ListOfTaskNames.append(TaskName.Name)
            print("Tasks found:\n")
            printList(ListOfTaskNames)
    elif optionChoice == "B" or optionChoice == "b": # Get a list of tasks, then tags
        try:
            ListOfPVNodes = getPLCTags(client)
        except Exception as exc:
            print('\n', exc)
            print("Get variables failed!")
        else:
            ListOfTagNames = []
            for PVNode in ListOfPVNodes:
                TagName = PVNode.get_browse_name()
                ListOfTagNames.append(TagName.Name)
            print("\nTags found:")
            printList(ListOfTagNames)
    elif optionChoice == "C" or optionChoice == "c": # Get a specific variable value
        taskName = input("Enter the name of the task as it exists on the PLC (use AsGlobalPV for Global variables): ")
        varName = input("Enter the name of the variable as it exists on the PLC: ")
        try:
            Value = getValueOfNode(client, taskName, varName)
        except:
            print("Get Value failed!")
        else:
            print("\nThe value of the chosen variable is: " + str(Value))
    elif optionChoice == "D" or optionChoice == "d": # Set a specific variable value
        taskName = input("Enter the name of the task as it exists on the PLC (use AsGlobalPV for Global variables): ")
        varName = input("Enter the name of the variable as it exists on the PLC: ")
        value = input("Enter the value to set: ")
        try:
            setValueOfNode(client, taskName, varName, value)
        except ValueError as ve:
            print(ve)
            print("Variable was not set!")
        except RuntimeError as re:
            print(re)
            print("Variable was not set!")
        except:
            print("Variable was not set!")
        else:
            print("Variable set successfully. The value is now:", getValueOfNode(client, taskName, varName))
    elif optionChoice == "E" or optionChoice == "e": # Import a list of vars
        # Get filenames from user
        inputCsvFileName = "/mnt/c/projects/Non AS Projects/Python/OpcUaUnitTesting/OpcUaUnitTesting/config/Inputs.csv" #input("Enter the path to a valid input file (CSV format): ")
        outputCsvFileName = "/mnt/c/projects/Non AS Projects/Python/OpcUaUnitTesting/outfiles/Output.csv" #input("Enter the path to where the output file should be saved: ")
        # Check for existing output file
        if exists(outputCsvFileName):
            ShouldIDeleteFile = input(("Output file already exists. The existing file will be overwritten. Continue? Y/N "))
            if ShouldIDeleteFile == 'Y' or ShouldIDeleteFile == 'y':
                pass
            elif ShouldIDeleteFile == 'N' or ShouldIDeleteFile == 'n':
                print("Aborting")
                return menu(client)
            else:
                print("Invalid input. Aborting")
                return menu(client)
        # Import CSV file and create a list of variables to get sorted by time
        ListOfInputs = importTestFile(inputCsvFileName)
        # Set initial values
        startTime = datetime.now()
        ListOfOutputs = []
        finishedVars = 0
        print("\nProcessing list of", len(ListOfInputs), "variables starting at", startTime)
        # Process list in order
        for CurrentVar in ListOfInputs:
            try:
                OutputEntry = processTestFileEntry(client, CurrentVar)
            except Exception as exc:
                logging.warning('Error processing line %i: %s', finishedVars + 1, exc)
            finally:
                ListOfOutputs.append(OutputEntry)
                finishedVars += 1
                print("Processed line", finishedVars, "of", len(ListOfInputs))
        # Export results
        try:
            exportValuesToTestFile(ListOfOutputs, outputCsvFileName)
        except Exception as exc:
            logging.warning('Failed to write output file: %s', exc)
        finally:
            print("Finished processing",finishedVars,"variables at",datetime.now())
    elif optionChoice == "Z" or optionChoice == "z": # Disconnect
        endMenu = True
    else: # Show error message
        print("\nSorry, that's not one of the available options")

    if endMenu:
        try:
            client.disconnect()
        except Exception as exc:
            print('\n', exc)
            print("Disconnection failed!")
        else:
            print("\nDisconnected!")
        finally:
            print("Thank you for using the OpcUa Unit Tester")
    else:
        return menu(client)

######## Main ########

def main():
    # Initialize logging
    logging.basicConfig(filename="OpcUaUnitTesting_Log.txt", level=logging.INFO, filemode="w")

    # Get connection parameters from the User
    clientIp = "172.20.16.1" #= input("Enter PLC IP Address: ")
    clientPort = "4840" #= input("Enter PLC OPC-UA port: ")
    clientUserName = "" #= input("Enter Username for connection, or leave blank for Anonymous connection: ")

    if clientUserName == "":
        clientPath = "opc.tcp://" + clientIp + ":" + clientPort
    else:
        clientPath = "opc.tcp://" + clientUserName + "@" + clientIp + ":" + clientPort
    print("Connecting to:", clientPath)

    # Define the Client using connection parameters
    client = Client(clientPath)

    # Try to make the connection to the Client
    try:
        client.connect()
    # Handle exceptions
    except ConnectionRefusedError:
        print("Connection refused (Error Number 111)")
        return
    except:
        print("Connection Failed!")
        return

    # When connection is successful, show the option menu
    menu(client)

if __name__ == '__main__':
    main()

# To Do:
# -Methods

# Example Notes
    # client = Client("opc.tcp://admin@localhost:4840") #connect using a user

    #root = client.get_root_node()
    #print("Objects node is: ", root)

    # Node objects have methods to read and write node attributes as well as browse or populate address space
    #print("Children of root are: ", root.get_children())

    # get a specific node knowing its node id
    #var = client.get_node(ua.NodeId(1002, 2))
    #var = client.get_node("ns=3;i=2002")
    #print(var)
    #var.get_data_value() # get value of node as a DataValue object
    #var.get_value() # get value of node as a python builtin
    #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
    #var.set_value(3.9) # set node value using implicit data type

    # Stacked myvar access
    # print("myvar is: ", root.get_children()[0].get_children()[1].get_variables()[0].get_value())

    # Possible variant types:
    # :ivar Null:
    # :ivar Boolean:
    # :ivar SByte:
    # :ivar Byte:
    # :ivar Int16:
    # :ivar UInt16:
    # :ivar Int32:
    # :ivar UInt32:
    # :ivar Int64:
    # :ivar UInt64:
    # :ivar Float:
    # :ivar Double:
    # :ivar String:
    # :ivar DateTime:
    # :ivar Guid:
    # :ivar ByteString:
    # :ivar XmlElement:
    # :ivar NodeId:
    # :ivar ExpandedNodeId:
    # :ivar StatusCode:
    # :ivar QualifiedName:
    # :ivar LocalizedText:
    # :ivar ExtensionObject:
    # :ivar DataValue:
    # :ivar Variant:
    # :ivar DiagnosticInfo:
