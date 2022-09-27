"""
OpcUaUnitTesting test script

Marcus Mangel <marcus.mangel@br-automation.com>

"""
from OpcUaUnitTesting import OpcUaUnitTesting
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
    logging.basicConfig(filename="OpcUaUnitTesting_TestScript_Log.log", level=logging.INFO, filemode="w")
    logging.getLogger("opcua").setLevel(logging.DEBUG)

    # Get connection parameters from the User
    clientIp = input("Enter PLC IP Address: ")
    clientPort = input("Enter PLC OPC-UA port: ")
    clientUserName = input("Enter Username for connection, or leave blank for Anonymous connection: ")
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
    with os.scandir('tests') as TestDir:
        for entry in TestDir:
            if not entry.name.startswith('!') and entry.is_dir():
                TestFolders.append(entry.name)

    # Run the test for each test directory
    TotalTests = 0;
    PassedTests = 0;
    FailedTests = 0;
    for TestDir in TestFolders:
        print("\nTesting", TestDir)
        inputCsvFileName = "tests/" + TestDir + "/Inputs.csv"
        outputCsvFileName = "tests/" + TestDir + "/Output.csv"
        correctOutputCsvFileName = "tests/" + TestDir + "/CorrectOutput.csv"
        testResultCsvFileName = "tests/" + TestDir + "/TestOutput.csv"
        OpcUaUnitTesting.processTestFile(client, inputCsvFileName, outputCsvFileName)

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

        TotalTests = TotalTests + 1
        if os.stat(testResultCsvFileName).st_size != 0:
            FailedTests = FailedTests + 1
            print("\nTest Failed!")
        else:
            PassedTests = PassedTests + 1
            print("\nTest Passed!")

    try:
        client.disconnect()
    except Exception as exc:
        print("\nDisconnection failed!", exc)
    else:
        print("\nDisconnected!")
    finally:
        print("Testing Complete!")
        print("Passed", PassedTests, "test(s) out of", TotalTests, "total")
        print("Failed", FailedTests, "test(s) out of", TotalTests, "total")

if __name__ == '__main__':
    main()
