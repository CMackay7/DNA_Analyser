# from tkinter import *
from tkinter.filedialog import asksaveasfilename

# This file just saves the file with the data in


def write_to_file(areas, maxes):
    whattowriteareas = construct_file(areas)
    whattowritemaxes = construct_file(maxes)
    filepath = asksaveasfilename()
    completefileareas = filepath + "areas.txt"
    completefilemaxes = filepath + "maxes.txt"
    filetowriteareas = open(completefileareas, "w+")

    for line in whattowriteareas:
        filetowriteareas.write(line)

    filetowritemaxes = open(completefilemaxes, "w+")

    for line in whattowritemaxes:
        filetowritemaxes.write(line)


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
