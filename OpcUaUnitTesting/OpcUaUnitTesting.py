"""
OpcUaUnitTesting main script

Marcus Mangel <marcus.mangel@br-automation.com>

"""

######## Import Libraries ########

import sys
from opcua import Client, ua, Node

######## Structure Declarations ########



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

# Gets the value of a variable on the PLC
# Requires An OpcUa Client, the name of a Task and the name of a Variable in that task
# Modifies: Only local variables
# Returns the value using OpcUa Client get_value() function
def getValueOfNode(client, taskName, varName):
    nodeName = "ns=6;s=::" + taskName + ":" + varName
    nodeAddress = client.get_node(nodeName)
    try:
        value = nodeAddress.get_value()
    except Exception as exc:
        print("\n", exc)
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
    nodeName = "ns=6;s=::" + taskName + ":" + varName
    node = client.get_node(nodeName)

    # Get the datatype of the node on the server
    variantType = node.get_data_type_as_variant_type()

    # User input must be cast to match server variable type
    if variantType == ua.VariantType.Boolean:
        pass
    elif variantType == ua.VariantType.SByte:
        try:
            value = int(value)
        except:
            raise ValueError("Invalid input. PLC variable is SByte")
            return
    elif variantType == ua.VariantType.Byte:
        try:
            value = int(value)
        except:
            raise ValueError("Invalid input. PLC variable is Byte")
            return
    elif variantType == ua.VariantType.Int16:
        try:
            value = int(value)
        except:
            raise ValueError("Invalid input. PLC variable is Int16")
            return
    elif variantType == ua.VariantType.UInt16:
        try:
            value = int(value)
        except:
            raise ValueError("Invalid input. PLC variable is UInt16")
            return
    elif variantType == ua.VariantType.Int32:
        try:
            value = int(value)
        except:
            raise ValueError("Invalid input. PLC variable is Int32")
            return
    elif variantType == ua.VariantType.UInt32:
        try:
            value = int(value)
        except:
            raise ValueError("Invalid input. PLC variable is UInt32")
            return
    elif variantType == ua.VariantType.Int64:
        try:
            value = int(value)
        except:
            raise ValueError("Invalid input. PLC variable is Int64")
            return
    elif variantType == ua.VariantType.UInt64:
        try:
            value = int(value)
        except:
            raise ValueError("Invalid input. PLC variable is UInt64")
            return
    elif variantType == ua.VariantType.Float:
        try:
            value = float(value)
        except:
            raise ValueError("Invalid input. PLC variable is Float")
            return
    elif variantType == ua.VariantType.Double:
        try:
            value = float(value)
        except:
            raise ValueError("Invalid input. PLC variable is Double")
            return
    elif variantType == ua.VariantType.String:
        pass
    elif variantType == ua.VariantType.DateTime:
        pass

    # Set the variable's value
    try:
        node.set_value(ua.DataValue(ua.Variant(value, variantType)))
    except Exception as exc:
        print("\n", exc)
        raise RuntimeError()
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
        taskName = "ServerTask" #= input("Enter the name of the task as it exists on the PLC: ")
        varName = "ExplicitIn" #= input("Enter the name of the variable as it exists on the PLC: ")
        value = input("Enter the value to set: ")
        try:
            setValueOfNode(client, taskName, varName, value)
        except ValueError as ve:
            print("\n", ve)
            print("Variable was not set!")
        except:
            print("Variable was not set!")
        else:
            print("Variable set successfully. The value is now: ", getValueOfNode(client, taskName, varName))
    elif optionChoice == "Z" or optionChoice == "z": # Disconnect
        endMenu = True
    else: # Show error message
        print("\nSorry, that's not one of the available options")

    if endMenu:
        try:
            client.disconnect()
        except Exception as exc:
            print("\n", exc)
            print("Disconnection failed!")
        else:
            print("\nDisconnected!")
        finally:
            print("Thank you for using the OpcUa Unit Tester")
    else:
        return menu(client)

######## Main ########

def main():
    # Get connection parameters from the User
    clientIp = "172.29.240.1" #= input("Enter PLC IP Address: ")
    clientPort = "4841" #= input("Enter PLC OPC-UA port: ")
    clientUserName = "" #= input("Enter Username for connection, or leave blank for Anonymous connection: ")

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
