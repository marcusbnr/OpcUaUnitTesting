"""
OpcUaUnitTesting main script

Marcus Mangel <marcus.mangel@br-automation.com>

"""

######## Import Libraries ########

import sys
from opcua import Client


######## Structure Declarations ########



######## Declare Functions ########

#
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
    ServerTasksRootNode = client.get_node("ns=6;s=::")
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
    ListOfTaskNodes = getPLCTasks(client)
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

#
def getValueOfNode(client, taskName, varName):
    nodeName = "ns=6;s=::" + taskName + ":" + varName
    nodeAddress = client.get_node(nodeName)
    try:
        value = nodeAddress.get_value()
    except RuntimeError as exc:
        print("\n", exc)
        raise RuntimeError("Get Value failed!")
        return 0
    else:
        return value

#
def setValueOfNode(client, taskName, varName, value):
    nodeName = "ns=6;s=::" + taskName + ":" + varName
    nodeAddress = client.get_node(nodeName)
    try:
        nodeAddress.set_value(value)
    except RuntimeError as exc:
        print("\n", exc)
        raise RuntimeError("Set Value failed!")
    return

# Function which shows the user a menu and processes responses
# Requires: An OpcUa Client
# Modifies: Only local variables
# Returns: Nothing
def menu(client):
    print("\nWelcome to the OpcUa Unit Tester! Please enter the letter corresponding to the desired option: ")
    print("A. Get a list of PLC tasks")
    print("B. Get a list of PLC variables by task")
    print("C. Get the value of a specific PLC variable")
    print("D. Set the value of a specific PLC variable")
    print("Z. Disconnect")
    optionChoice = input()
    endMenu = False

    if optionChoice == "A" or optionChoice == "a": # Get list of tasks as nodes
        ListOfTaskNodes = getPLCTasks(client)
        ListOfTaskNames = []
        for Task in ListOfTaskNodes:
            TaskName = Task.get_browse_name()
            ListOfTaskNames.append(TaskName.Name)
        print("Tasks found:\n")
        printList(ListOfTaskNames)
    elif optionChoice == "B" or optionChoice == "b": # Get a list of tasks, then tags
        ListOfPVNodes = getPLCTags(client)
        ListOfTagNames = []
        for PVNode in ListOfPVNodes:
            TagName = PVNode.get_browse_name()
            ListOfTagNames.append(TagName.Name)
        print("\nTags found:")
        printList(ListOfTagNames)
    elif optionChoice == "C" or optionChoice == "c": # Get a specific variable value
        taskName = input("Enter the name of the task as it exists on the PLC: ")
        varName = input("Enter the name of the variable as it exists on the PLC: ")
        try:
            Value = getValueOfNode(client, taskName, varName)
        except:
            print("Get Value failed!")
        else:
            print("\nThe value of the chosen variable is: " + str(Value))
    elif optionChoice == "D" or optionChoice == "d": # Set a specific variable value
        taskName = input("Enter the name of the task as it exists on the PLC: ")
        varName = input("Enter the name of the variable as it exists on the PLC: ")
        value = input("Enter the value to set: ")
        try:
            setValueOfNode(client, taskName, varName, value)
        except:
            print("Variable was not set!")
    elif optionChoice == "Z" or optionChoice == "z": # Disconnect
        endMenu = True
    else: # Show error message
        print("\nSorry, that's not one of the available options")

    if endMenu:
        client.disconnect()
        print("\nDisconnected! Thank you for using the OpcUa Unit Tester")
    else:
        return menu(client)

######## Main ########

def main():
    # Get connection parameters from the User
    clientIp = input("Enter PLC IP Address: ")
    clientPort = input("Enter PLC OPC-UA port: ")
    clientUserName = input("Enter Username for connection, or leave blank for Anonymous connection: ")

    if clientUserName == "":
        clientPath = "opc.tcp://" + clientIp + ":" + clientPort
    else:
        clientPath = "opc.tcp://" + clientUserName + "@" + clientIp + ":" + clientPort
    print(clientPath)

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
