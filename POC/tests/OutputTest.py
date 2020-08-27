"""
Instructions:
python3 OutputTest.py <graph-folder-name> <naive-output-file-name> <synthetic-data-file-name>

This script will compare both text files (naive output and synthetic data). A match/unmatch value will be appeneded at
each time step to outline which active paths have been evaluated correctly or incorrectly.

The files are compared line by line. When an active component is detected, it is sorted in both files and compared for
equality.
"""

# Get graph path from input
import ast
import re
import sys

# Graph path
graphPath = "../" + str(sys.argv[1])

# Algorithm output file path
outputPath = graphPath + "/Data/" + str(sys.argv[2])

# Synthetic data file path
syntheticDataPath = graphPath + "/Data/" + str(sys.argv[3])

# Time stamp of input file, will be used to name the output file
tStamp = re.search("([0-9]{2}\-[0-9]{2}\-\-[0-9]{2}\-[0-9]{2}\-[0-9]{2})", str(sys.argv[2]))[0]


def main():

    # Final result of the test.
    testFailed = False

    # Keeps track of the line number
    lineNumber = 1

    # Result of testing each time step
    testResult = open(graphPath +"/Data/" + tStamp + "-test-result.txt", "w")

    # Get the contents of the synthetic data file
    syntheticDataFile = open(syntheticDataPath, 'r')
    syntheticDataFileLines = syntheticDataFile.readlines()

    # Open the output file
    with open(outputPath, 'r') as outPutFile:

        # List of the active components per time step extracted from the output file
        outPutComponentList = []

        # List of the active components per time step extracted from the synthetic data file
        dataComponentList = []

        # Keeps track of the current time step
        currentTS = ""

        for line in outPutFile:
            print("line number: " + str(lineNumber))

            # Strip line from output file
            strippedLine = line.strip()

            # Extract the time step number
            if strippedLine.startswith('ts_'):
                currentTS = strippedLine

            # If this is a line of an active component, do the following:
            if strippedLine[0] == "{":
                print(strippedLine)

                # Extract active component from the output file (always starts with '{')
                component_output = ast.literal_eval("[" + strippedLine[1:len(strippedLine) - 1] + "]")
                print("converted to list")

                # Sort the active component
                component_output.sort()

                # Extract the active component from BFS output


                # Extract the active component from the synthetic data file
                strippedLine_data = syntheticDataFileLines[lineNumber - 1].strip()
                print("synthetic data: ")
                print(strippedLine_data)
                component_data = ast.literal_eval("[" + strippedLine_data[1:len(strippedLine_data) - 1] + "]")

                # Sort the active component
                # print(component_data)
                component_data.sort()

                # Aggregate active components to their respective lists
                outPutComponentList.append(component_output)
                dataComponentList.append(component_data)

            # If this is not a line of an active component, do the following:
            else:
                # if any active component was found in the current time step:
                if len(outPutComponentList) > 0 or len(dataComponentList) > 0:

                    # Write each active component for each time step
                    testResult.write(currentTS + "\n")
                    testResult.write("Output List: line " + str(lineNumber) + ":\n" + str(outPutComponentList) + "\n")
                    testResult.write("Data List: line " + str(lineNumber) + ":\n" + str(dataComponentList) + "\n")

                    # Compare the active components found in the output file and the synthetic data file
                    if sorted(outPutComponentList) == sorted(dataComponentList):
                        testResult.write("Match!\n--------------------\n")
                    else:
                        testResult.write("Fail!\n--------------------\n")
                        testFailed = True

                    outPutComponentList = []
                    dataComponentList = []

                # if no active components were found in current time stamp, simply move to the next line.

            lineNumber = lineNumber + 1

    testResult.close()
    syntheticDataFile.close()

    # If any component does not much, test fails.
    if testFailed:
        print("Some timestamps do not match!")
    else:
        print("Success!")


main()