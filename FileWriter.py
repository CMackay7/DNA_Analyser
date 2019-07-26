from tkinter import *
import os.path

# This file just saves the file with the data in

root = Tk()

filename = "untitled.txt"
# CHANGE THIS TO SPECIFY WHERE FILE GOES
filepath = "C:/Users/camer/Desktop/Christie Data/"


def write_to_file(lines):
    global filename
    whattowrite = construct_file(lines)
    get_input()
    completefile = os.path.join(filepath, filename)
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


# Using Tkinter to get the file name from the user
def get_input():
    textBox = Entry(root, width=10)
    textBox.pack()
    buttonCommit = Button(root, height=1, width=10, text="Commit",
                          command=lambda: retrieve_input(textBox))
    # command=lambda: retrieve_input() >>> just means do this when i press the button
    buttonCommit.pack()

    mainloop()


def retrieve_input(textBox):
    global filename
    filename = (textBox.get() + ".txt")
    root.quit()
