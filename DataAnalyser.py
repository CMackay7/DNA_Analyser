import operator
import GraphAnalysis
import FileWriter
import matplotlib.pyplot as plt
import numpy as np
from numpy import trapz


def some_testing(data, centroids, image, spacing, intents):
    splits, datas = split_into_sections(data)
    simple_graphing(data, splits)
    get_areas(datas)


    # split_into_sections takes the data will call go_along_data in GraphAnalysis and will find the first middle and last
    # peak in the data. It passes back the position of the cuts and the cuts as they are both need at some point
    # Will be cleaned up more at a later date
def split_into_sections(data):
    toadd = []
    final = []
    for i in range(len(data)):
        for x in range(2):
            use = data[i]
            if x == 0:
                op = operator.add
                length = 0
            else:
                op = operator.sub
                length = len(use) - 1
            point = GraphAnalysis.go_along_data(use, length, op)
            toadd.append(point)
        final.append(toadd[:])
        toadd.clear()
    print()
    returnsections = []
    passback = []

    # Work out the peaks
    for i in range(len(final)):
        firstpeak = data[i][0:final[i][0]]
        middlepeak = data[i][final[i][0]:final[i][1]]
        lastpeak = data[i][final[i][1]: len(data[i])]
        returnsections.append(firstpeak)
        returnsections.append(middlepeak)
        returnsections.append(lastpeak)
        passback.append(returnsections[:])
        returnsections.clear()
    return final, passback


# This is called from get_intensity and takes the data generated by it and will make simple graphs from the data
# the Y axis is the intensity and the X axis is the pixel number (basically depth)
def simple_graphing(data, centroidedges):
    for i in range(len(data)):

        data_point = data[i]
        title = ("Lane " + str(i))
        count = []
        for x in range(len(data_point)):
            count.append(x)

        fig, ax = plt.subplots()
        ax.plot(count, data_point)
        fig.suptitle(title)

        plt.axvline(x=0)
        plt.axvline(x=centroidedges[i][0])
        plt.axvline(x=centroidedges[i][1])
        plt.axvline(x=len(data[i]) - 1)
        plt.show()
        # Uncomment this so show graphs


def get_areas(datas):
    areas = []
    for data in datas:
        toadd = []
        for i in data:
            y = np.array(i)
            area = trapz(y, dx=1)
            toadd.append(area)
        areas.append(toadd[:])
        toadd.clear()

    normalise_values(areas)


def normalise_values(data):
    import FileWriter
    normalised_values = []
    for values in data:
        toadd = []
        total = sum(values)
        toadd.append(round((values[0] / total)*100, 2))
        toadd.append(round((values[1] / total)*100, 2))
        toadd.append(round((values[2] / total)*100, 2))
        normalised_values.append(toadd[:])
        toadd.clear()

    FileWriter.write_to_file(normalised_values)
