"""
OpcUaUnitTesting test script

Marcus Mangel <marcus.mangel@br-automation.com>

"""

from OpcUaUnitTesting import processTestFile
import sys
import os
from os.path import exists
import logging
from opcua import Client, ua, Node
from datetime import datetime
import csv

######## Main ########

def main():
    # Initialize logging
    logging.basicConfig(filename="OpcUaUnitTesting_Log.log", level=logging.INFO, filemode="w")
    logging.getLogger("opcua").setLevel(logging.WARNING)

    # Get connection parameters from the User
    clientIp = '172.18.224.1' #input("Enter PLC IP Address: ")
    clientPort = '4840' #input("Enter PLC OPC-UA port: ")
    clientUserName = "" #input("Enter Username for connection, or leave blank for Anonymous connection: ")
    clientPassWord = ""
    if clientUserName == "":
        clientPath = "opc.tcp://" + clientIp + ":" + clientPort
        printableClientPath = clientPath
    else:
        clientPassWord = input("Enter Password for connection: ")
        clientPath = "opc.tcp://" + clientUserName + ":" + clientPassWord + "@" + clientIp + ":" + clientPort
        printableClientPath = "opc.tcp://" + clientUserName + "@" + clientIp + ":" + clientPort # Don't print password

    # Define the Client using connection parameters
    client = Client(clientPath)

    # Try to make the connection to the Client
    print("Connecting to:", printableClientPath)
    try:
        client.connect()
    # Handle exceptions
    except Exception as exc:
        print("Connection Failed!", exc)
        return

    # Find test directories
    TestFolders = []
    with os.scandir('/mnt/c/projects/Non AS Projects/Python/OpcUaUnitTesting/tests') as TestDir:
        for entry in TestDir:
            if not entry.name.startswith('!') and entry.is_dir():
                TestFolders.append(entry.name)

    # Run the test for each test directory
    for TestDir in TestFolders:
        print("\nTesting", TestDir)
        inputCsvFileName = "/mnt/c/projects/Non AS Projects/Python/OpcUaUnitTesting/tests/" + TestDir + "/Inputs.csv"
        outputCsvFileName = "/mnt/c/projects/Non AS Projects/Python/OpcUaUnitTesting/tests/" + TestDir + "/Output.csv"
        correctOutputCsvFileName = "/mnt/c/projects/Non AS Projects/Python/OpcUaUnitTesting/tests/" + TestDir + "/CorrectOutput.csv"
        testResultCsvFileName = "/mnt/c/projects/Non AS Projects/Python/OpcUaUnitTesting/tests/" + TestDir + "/TestOutput.csv"
        processTestFile(client, inputCsvFileName, outputCsvFileName)

        # Compre files
        with open(outputCsvFileName, 'r') as ScriptOutput, open(correctOutputCsvFileName, 'r') as CorrectOutput:
            ScriptOutputLines = ScriptOutput.readlines()
            CorrectOutputLines = CorrectOutput.readlines()
            ScriptOutput.close()
            CorrectOutput.close()

        with open(testResultCsvFileName, 'w') as outFile:
            for line in CorrectOutputLines:
                if line not in ScriptOutputLines:
                    outFile.write(line)
            outFile.close()

        if os.stat(testResultCsvFileName).st_size != 0:
            print("\nTest Failed!")
        else:
            print("\nTest Passed!")

    try:
        client.disconnect()
    except Exception as exc:
        print("Disconnection failed!", exc)
    else:
        print("Disconnected!")
    finally:
        print("Testing Complete!")

if __name__ == '__main__':
    main()
