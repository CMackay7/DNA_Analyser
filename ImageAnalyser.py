# This file is used for finding and extracting the intensity data from the image. It handles finding th eedges
# of the dna and getting the brightness
import DataAnalyser
import ImageManipulation
import cv2
from tkinter import *
import GraphAnalysis
import statistics


root = Tk()


# Get intensity is passed the image and the lines. It will run along the pixels in each line and get the intensity
# of each pixel adds all the intensities to a list
def get_intensity(image, centroids):
    list_of_dna = get_drop_off(centroids, image)
    dna_height_data = find_vertical_edges(centroids, image, list_of_dna)
    spacings = max_spacing_lines(dna_height_data)
    centroids = extend_points(centroids, image, spacings)

    ImageManipulation.draw_lanes(centroids, image.copy())
    cv2.imshow('testimage', ImageManipulation.draw_lanes(centroids, image.copy()))
    cv2.waitKey(0)
    single_row_intensities = []
    all_intensities = []

    for point in centroids:
        lengthofcent = len(point)
        start = point[0][0]
        end = point[lengthofcent - 1][0]
        y = point[0][1]

        counter = 0
        for i in range(start, end):
            addintensity = 0
            points = spacings[counter]
            for yedit in range(points[0], points[1]):
                # The intensity of the image is calculated by taking the values for red blue and green and summing the
                # values.
                r, b, g = image[y, i]
                r = int(r)
                b = int(b)
                g = int(g)
                # Convert to int so it doesn't get an error
                intensity = int(r + b + g)
                addintensity = addintensity + intensity
                # Store values in lists
            single_row_intensities.append(addintensity)
        counter += 1
        all_intensities.append(single_row_intensities[:])
        single_row_intensities.clear()
    tosend = decrease_values(all_intensities)
    DataAnalyser.some_testing(tosend, centroids, image, spacings, list_of_dna)


# Sorts centroids
def sort_cent(cent):
    sorted_centroids = sorted(cent, key=lambda x: x[0])
    return sorted_centroids


# This function makes sure that the whole light spot (left and right) will get analysed
# it will extend the length of the line until there is no more light and therefore not the dna
def extend_points(centroids, image, spacing):
    backgrounds = calc_background(centroids, image, spacing)
    to_add = []
    to_be_added_to = []
    _, width, _ = image.shape
    counter = 0
    # Loop through the lines, extend the first point on each line until it is no longer on the dna, do the same
    # with the last point on the line
    for cent in centroids:

        cent = sort_cent(cent)
        cent_len = len(cent)
        for i in range(cent_len):
            top = spacing[counter][0]
            bottom = spacing[counter][1]
            x = cent[i][0]
            y = cent[i][1]
            background = backgrounds[counter]
            # If first point go here
            if i == 0:
                end_hit = False
                changer = 1
                while not end_hit:
                    totalint = 0
                    for changey in range(top, bottom):
                        r, b, g = image[y + changey, x - changer]
                        intent = pixel_intent(r, g, b)
                        totalint = totalint + intent
                    if totalint <= background or x - changer == 0:
                        end_hit = True
                    else:
                        changer = changer + 1
                edited_point = (x - changer, cent[0][1])
                # If it is the final point go here
            elif i == cent_len - 1:
                end_hit = False
                changer = 1
                while not end_hit:
                    totalint = 0
                    for changey in range(top, bottom):
                        r, b, g = image[y + changey, x + changer]
                        intent = pixel_intent(r, g, b)
                        totalint += intent
                    if totalint <= background or cent[i][0] + changer == width - 1:
                        end_hit = True
                    else:
                        changer = changer + 1
                edited_point = (cent[i][0] + changer, cent[i][1])
                # If it is neither it means the point is in the middle of the line, therefore it doesnt need changing
                # so just copy it over
            else:
                edited_point = cent[i]
            to_add.append(edited_point)
        counter += 1
        to_be_added_to.append(to_add[:])
        to_add.clear()
    return to_be_added_to


# Given red, blue and green values for a pixel it converts it to integers and sums them, it doesnt do
# a lot of computation but it gets called a lot so it saves space
def pixel_intent(r, g, b):
    r = int(r)
    b = int(b)
    g = int(g)
    # Convert to int so it doesn't get an error
    intensity = int(r + b + g)
    return intensity


# Just use to decrease values that are in background to 0 so middle values doesn't get free area
# for now it will just -1500 (generally what I've seen as the cut off between on cells and not)
# hopefully this will be changed later
def decrease_values(data):
    newvals = []
    toreturn = []
    for intensityrow in data:
        background = GraphAnalysis.get_background_signal(intensityrow)
        for x in intensityrow:
            if x - background <= 0:
                newvals.append(0)
            else:
                newvals.append(x - background)
        toreturn.append(newvals[:])
        newvals.clear()
    return toreturn


# This method will work out the intensity of the center of a dna spot. This is used when the edges of the
# dna needs to be calculated it makes it easier to tell based of intensity when a pixed that is not on the dna
# spot has been hit.
def get_drop_off(centroids, image):
    avg_int = 0
    count = 0
    total_int = 0
    final_list = []
    list_of_intent = []
    # Loop through lines and then points on each line
    for cent in centroids:
        for point in cent:
            r, b, g = image[point[1], point[0]]
            intent = pixel_intent(r, g, b)
            total_int += intent
            count += 1
            list_of_intent.append(intent)

        avg_int += total_int
        total_int = 0
        final_list.append(list_of_intent[:])
        list_of_intent.clear()
    avg_int = avg_int/count

    return final_list


# (top, bottom)
# This method find the top and bottom point for one line of dna, used to make sure the whole profile of the dna
# is read and not just one line.
def find_vertical_edges(centroids, image, listint):
    changer = 0
    dna_edges = []
    line_points_to_add = []
    arraycount = 0
    intcount = 0
    linecount = 0
    for cent in centroids:
        currline = listint[linecount]
        for point in cent:
            is_hit = False
            bottom = 0
            currintent = currline[intcount]
            arraycount += 1
            # Loop going down in the image (+1) and if the brightness goes down 15% from the middle
            # intensity store the position
            while not is_hit:
                changer += 1
                r, b, g = image[point[1] + changer, point[0]]
                intent = pixel_intent(r, g, b)
                if intent < (currintent - currintent * 0.15):
                    bottom = changer
                    is_hit = True
                    changer = 0
            is_hit = False

            # Do the same again but going up in the image
            while not is_hit:
                changer += 1
                r, b, g = image[point[1] - changer, point[0]]
                intent = pixel_intent(r, g, b)
                if intent < (currintent - currintent * 0.15):
                    top = -changer
                    spacing = (top, bottom)
                    is_hit = True
                    changer = 0

            # Add the top and bottom
            line_points_to_add.append(spacing[:])
            intcount += 1
        dna_edges.append(line_points_to_add[:])
        line_points_to_add.clear()
        intcount = 0
        linecount += 1
    return dna_edges


# This method takes the output of extend_DNA_spots and will work out the widest gap (lowest bottom and highest top) in
# order to make sure non of the dna spot it missed
def max_spacing_lines(spacings):
    new_spacings = []
    for one_line in spacings:
        counter = 0
        max_top = 0
        max_bottom = 0
        for point in one_line:
            top = point[0]
            bottom = point[1]
            if top < max_top:
                max_top = top
            if bottom > max_bottom:
                max_bottom = bottom
            counter += 1
        new_spacings.append((top, bottom))
    return new_spacings


# This function is used ot help find the edges of the dna spots. It calculates the average brightness of each lane in
# the image. When checking if a pixel is part of the background the pixel intensity can be compared to this value.
def calc_background(centroids, image, spacings):
    intlist = []
    baselist = []
    height, width, _ = image.shape
    count = 0
    for cent in centroids:
        total = 0
        for x in range(0, width - 1):
            for changer in range(spacings[count][0], spacings[count][1]):
                r, g, b = (image[cent[0][1] + changer, x])
                pixel_intent(r, g, b)
                total += pixel_intent(r, g, b)

            intlist.append(total)
            total = 0
        count = 0
        baselist.append(intlist[:])
        intlist.clear()

    avg_lane_brightness = []
    for point in baselist:
        sorted_data = sorted(point, reverse=True)
        avg = statistics.mean(sorted_data)
        avg_lane_brightness.append(avg)

    return avg_lane_brightness
