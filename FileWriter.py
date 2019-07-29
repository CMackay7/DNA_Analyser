# from tkinter import *
from tkinter.filedialog import asksaveasfilename

# This file just saves the file with the data in


def write_to_file(lines):
    whattowrite = construct_file(lines)
    filepath = asksaveasfilename()
    completefile = filepath + ".txt"
    filetowrite = open(completefile, "w+")

    for line in whattowrite:
        filetowrite.write(line)


def construct_file(lines):
    onelane = []
    breaknames = ["open circular", "linear", "supercoiled"]

    # Construct file
    for i in range(len(lines)):

        onelane.append("DNA damage breakdown for lane " + str(i) + "\n")
        for x in range(3):
            onelane.append(breaknames[x] + ": " + str(lines[i][x]) + "%" + "\n")

        onelane.append("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + "\n")

    return onelane
