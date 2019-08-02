from tkinter.filedialog import asksaveasfilename
# This file just saves the file with the data in


def get_file():
    filepath = asksaveasfilename(title="Select save area")
    return filepath


# Write the results from each lane to file
def write_to_file(areas, maxes, filepath):
    whattowriteareas = construct_file(areas)
    whattowritemaxes = construct_file(maxes)
    completefileareas = filepath + "areas.txt"
    completefilemaxes = filepath + "maxes.txt"
    filetowriteareas = open(completefileareas, "w+")

    for line in whattowriteareas:
        filetowriteareas.writelines(line)

    filetowritemaxes = open(completefilemaxes, "w+")

    for line in whattowritemaxes:
        filetowritemaxes.writelines(line)


def construct_file(lines):
    onelane = []
    firstlane = "LANE    OC       L       SC\n"
    onelane.append(firstlane)
    # Construct file
    for i in range(len(lines)):
        onelane.append(str(i) + "      " + str(lines[i][0]) + "    " + str(lines[i][1]) + "    " + str(lines[i][2]) + "\n")

    return onelane
