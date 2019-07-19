import ClickHandler
import cv2
from tkinter.filedialog import askopenfilename
import Edditor
import ImageManipulation


# This method is where all current code should go to get inputs from the user
# Select image opens a file explorer using tkinter and returns the file path.

# Crop image allows the user to crop the image. It uses cropper to record the clicks
# then given the position of the clicks crops the image to this size

# Delete lines loops and when the user clicks a line it will remove it from centroids


def select_image():
    filename = askopenfilename()
    return filename


# Loops until the user exits with 'q' or they click and let go of the mouse
# it will display to the user a black square of where the crop if going to be
# if the user is happy with it then they can press 'y' to crop the image
# if not they can press 'r' and try the crop again
def crop_image(image_copy):
    cropper = ClickHandler.ClickHandler()
    clone = image_copy.copy()
    image_to_edit = image_copy.copy()
    while True:
        cv2.imshow('image_to_crop', image_to_edit)
        cv2.setMouseCallback("image_to_crop", cropper.click_and_crop)
        stay_in_loop = True
        # Stay in loop until they have quit or select section to crop
        while stay_in_loop:
            key = cv2.waitKey(1)
            if cropper.size() > 2:
                cropper.clear()
            if (cropper.size() == 2) or (key == ord("q")):
                stay_in_loop = False

        if key == ord("q"):
            break

        point1 = cropper.get()
        point2 = cropper.get()
        point1, point2 = check_crop_points(point1, point2)

        # Display the area the user has chosen to crop to see if they are alright with this
        cv2.rectangle(image_to_edit, point1, point2, (0, 255, 0), 2)
        cv2.imshow("image_to_crop", image_to_edit)

        stay_in_loop = True
        while stay_in_loop:
            key = cv2.waitKey(0)

            # If not reset the image
            if key == ord("r"):
                image_to_edit = clone.copy()
                cropper.clear()
                stay_in_loop = False

            # If they are happy crop the image
            elif key == ord("y") or key == ord("Y"):
                cv2.destroyAllWindows()
                return point1, point2


# Loop indefinitely, every time the user clicks on the screen call find_and_delete in Editor
# it will check if the user clicked a line and if they did will delete the line
# Will leave loop when the user presses 'q'
def delete_lanes(centroid_group, image):
    while True:
        get_click = ClickHandler.ClickHandler()
        cv2.setMouseCallback("lineimage", get_click.standard_click)
        stay_in_loop = True
        while stay_in_loop:
            key = cv2.waitKey(1)
            if (get_click.size() == 1) or (key == ord("q")):
                stay_in_loop = False

        if key == ord("q"):
            return centroid_group

        clicked_pos = get_click.get()
        return_centroids = Edditor.find_and_delete_lanes(centroid_group, clicked_pos)
        edited_image = ImageManipulation.draw_lanes(return_centroids, image.copy())
        cv2.destroyAllWindows()
        cv2.imshow('lineimage', edited_image)


# Used to remove the actual points that make up the line. Very similar to delete lines
# The user clicks on a centroid and it will be remove from the list of centroids and the image
def delete_points(centroids, image):
    while True:
        get_click = ClickHandler.ClickHandler()
        cv2.setMouseCallback("centroids_plotted", get_click.standard_click)
        stay_in_loop = True
        while stay_in_loop:
            key = cv2.waitKey(1)
            if get_click.size() == 1 or (key == ord("q")):
                stay_in_loop = False

        if key == ord("q"):
            return centroids

        clicked_pos = get_click.get()
        returned_centroids = Edditor.find_and_delete_centroids(centroids, clicked_pos)
        edited_image = ImageManipulation.draw_centroids(returned_centroids, image.copy())
        cv2.destroyAllWindows()
        cv2.imshow("centroids_plotted", edited_image)


# This is used so the user can add lines to the image, it takes and image and the centroids.
# When it picks up that the user has drawn a line (pressed the mouse down moved the mouse and let go)
# it will take the position of the clicks and add the two points to the list of centroids
def add_points_for_line(centroids, image):
    clone = image.copy()
    while True:
        get_click = ClickHandler.ClickHandler()
        cv2.setMouseCallback('addLines', get_click.click_and_crop)
        stay_in_loop = True
        while stay_in_loop:
            key = cv2.waitKey(1)
            if get_click.size() == 2 or key == ord('q'):
                stay_in_loop = False

        if key == ord("q"):
            return centroids

        point1 = get_click.get()
        point2 = get_click.get()
        point1, point2 = check_drawn_lines(point1, point2)
        centroids = Edditor.add_line(centroids, point1, point2)
        image = ImageManipulation.draw_lanes(centroids, clone.copy())
        cv2.destroyAllWindows()
        cv2.imshow('addLines', image)


# Was getting errors if they didn't draw the crop section from left to right
# this just swaps the function so it doesnt crash
def check_crop_points(point1, point2):
    point1_X = point1[0]
    point1_Y = point1[1]
    point2_X = point2[0]
    point2_Y = point2[1]

    if point2_Y < point1_Y:
        temp = point1_Y
        point1_Y = point2_Y
        point2_Y = temp
    if point2_X < point1_X:
        temp = point1_X
        point1_X = point2_X
        point2_X = temp

    return (point1_X, point1_Y), (point2_X, point2_Y)


# When the user draws another line it needs to be going from left to right, if they draw it the
# other way round they will flip the points
def check_drawn_lines(point1, point2):
    point1_X = point1[0]
    point2_X = point2[0]

    if point2_X < point1_X:
        return point2, point1

    return point1, point2
