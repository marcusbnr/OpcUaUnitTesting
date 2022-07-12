"""
OpcUaUnitTesting main script

Marcus Mangel <marcus.mangel@br-automation.com>

"""

######## Import Libraries ########
import sys
from opcua import Client


######## Structure Declarations ########



######## Declare Functions ########



######## Main ########

def main():
    client = Client("opc.tcp://172.27.112.1:4841")
    # client = Client("opc.tcp://admin@localhost:4840") #connect using a user

    try:
        client.connect()

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
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

        # Get list of tasks as nodes
        ServerTasksRootNode = client.get_node("ns=6;s=::")
        ListOfTaskNodes = ServerTasksRootNode.get_children()
        ListOfTaskNames = []
        for Task in ListOfTaskNodes:
            TaskName = Task.get_browse_name()
            ListOfTaskNames.append(TaskName.Name)

        print("Tasks found:\n")
        ListIndex = 0
        while ListIndex < len(ListOfTaskNames):
            print(ListIndex, ":", ListOfTaskNames[ListIndex])
            ListIndex += 1

        TaskToSearch = input("Input the number of the task to examine: ")
        ListOfPVNodes = ListOfTaskNodes[int(TaskToSearch)].get_children()
        ListOfTagNames = []
        for PVNode in ListOfPVNodes:
            TagName = PVNode.get_browse_name()
            ListOfTagNames.append(TagName.Name)

        print("Tags found:\n")
        ListIndex = 0
        while ListIndex < len(ListOfTagNames):
            print(ListIndex, ":", ListOfTagNames[ListIndex], "-", ListOfPVNodes[ListIndex].get_value())
            ListIndex += 1

    except ConnectionRefusedError:
        print("Connection refused (Error Number 111)")

    finally:
        client.disconnect()

if __name__ == '__main__':
    main()
