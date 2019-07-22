# After centroids work and are placed evenly what needs to be done before analysis
# 3.Allow users to add missing lines

# Stuff to do after analysis
# Create a UI


import UserInputHandler
import cv2
import ImageAnalyser


# This function will probably get changes to make it more more precise
# Currently reads in an image crops it then turns it into a binary image in order to find the contours
def curr_main():
    BaseImageDirec = UserInputHandler.select_image()
    # Need to read load in multiple copies of the same image, some of the operations done on images need to be done
    # on gray scale images some need to be in colour so need to read the same image in multiple ways
    standard_image = cv2.imread(BaseImageDirec)
    grey_image = cv2.imread(BaseImageDirec, cv2.CV_8UC1)

    inverted_image = cv2.bitwise_not(grey_image)

    # If you change the scale of the image you will have to change the pixel size in user ImageAnalyser
    inverted_image = cv2.resize(inverted_image, (960, 540))
    grey_image = cv2.resize(grey_image, (960, 540))
    standard_image = cv2.resize(standard_image, (960, 540))

    # Crop all images
    point1, point2 = UserInputHandler.crop_image(inverted_image)
    roi = inverted_image[point1[1]:point2[1], point1[0]:point2[0]]
    standard_image = standard_image[point1[1]:point2[1], point1[0]:point2[0]]
    grey_image = grey_image[point1[1]:point2[1], point1[0]:point2[0]]

    cv2.imshow('cropped', grey_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Reduce the noise of the image
    nonoise = cv2.fastNlMeansDenoising(roi, None, 10, 7, 21)

    # Changed to binary image
    binary_image = cv2.adaptiveThreshold(nonoise, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY
                                         , 25, 2)

    # Find the centers of the spots on the image
    centroids = find_centroids(binary_image.copy())
    drawn_centroids = draw_centroids(centroids, binary_image.copy())

    # Display to user
    cv2.imshow('centroids_plotted', drawn_centroids)
    key = cv2.waitKey(0)

    # Allow users to edit the centroids
    final_centers = centroids
    if key == ord('e'):
        forusecent = binary_image.copy()
        final_centers = UserInputHandler.delete_points(centroids, forusecent)

    # Find lanes and display on image
    grouped_centroids = find_lanes(final_centers, grey_image)
    lined_image = draw_lanes(grouped_centroids, grey_image.copy())
    cv2.imshow('lineimage', lined_image)
    key = cv2.waitKey(0)

    # Let the user edit the lines on the image
    final_centroids = grouped_centroids
    if key == ord('e'):
        final_centroids = UserInputHandler.delete_lanes(grouped_centroids, grey_image.copy())

    # cv2.destroyAllWindows()
    lined_image = draw_lanes(final_centroids, grey_image.copy())
    cv2.imshow('addLines', lined_image)

    # Allow them to press "e" if they want to add lines
    key = cv2.waitKey(0)
    if key == ord("e"):
        final_centroids = UserInputHandler.add_points_for_line(grouped_centroids, grey_image.copy())
    # final_centroids = Edditor.let_them_edit(grouped_centroids, foruseing)

    ImageAnalyser.get_intensity(standard_image, final_centroids)


# todo: improve the description of this function
# Find where the lanes are in the image given the centroids
# Given a sorted list of the centroids it will loop through and if a point
# is on the same position on the y axis (can be 5 pixels out) then it is added
# to the same list ast the last point.
# Otherwise it will add the points that are in the same line to a list clear the list
# and start looping through again
def find_lanes(centroids, image):
    sorted_centroids = sorted(centroids, key=lambda x: x[1])
    last_centroid_y = sorted_centroids[0][1]
    _, width = image.shape
    curr_list = []
    grouped_centroids = []
    for curr_point in sorted_centroids:
        modified_y_pos = curr_point[1] - 5
        if modified_y_pos < last_centroid_y:
            curr_list.append(curr_point)
        else:
            # Add points at the start and end of the image to the line spans the whole image
            grouped_centroids.append(curr_list[:])
            curr_list.clear()
            curr_list.append(curr_point)
            last_centroid_y = curr_point[1]

    return grouped_centroids


# Couldn't find a good way to one line going through multiple points on opencv
# so I loop through the centroids and plot lines going through individually
def draw_lanes(centroid_points, image):
    for centroid_group in centroid_points:
        sorted_point = sorted(centroid_group, key=lambda x: x[0])
        cv2.line(image, sorted_point[0], sorted_point[len(sorted_point) - 1], (255, 0, 255), 1)
    return image


def draw_centroids(centroids, image):
    # For each centroid on the image draw a cicle round it. Radius of the circle is 10
    for point in centroids:
        # I draw a black empty circle in the centroid position
        cv2.circle(image, point, 10, (13, 3, 94))
    return image


# Use openCV to find the dna points on the image
def find_centroids(image):
    contours0, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    moments = [cv2.moments(cnt) for cnt in contours0]

    # Given the moments of the image calculate where the center points are
    centroids = []
    for m in moments:
        if m['m10'] != 0.0 or m['m00'] != 0.0 or m['m01'] != 0.0:
            centroids.append((int(round(m['m10'] / m['m00'])), int(round(m['m01'] / m['m00']))))

    return centroids


if __name__ == '__main__':
    curr_main()
