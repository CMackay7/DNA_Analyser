# from tkinter import *
from tkinter.filedialog import asksaveasfilename

# This file just saves the file with the data in


filename = "untitled.txt"
# CHANGE THIS TO SPECIFY WHERE FILE GOES
filepath = "C:/Users/camer/Desktop/Christie Data/"


def write_to_file(lines):
    global filename
    whattowrite = construct_file(lines)
    fileypath = asksaveasfilename()
    completefile = fileypath + ".txt"
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

