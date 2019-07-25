
from queue import Queue
import cv2

# This class is used to handle the user clicking the image. To use it declare an instance of the clickhandler
# that will give you access to all the methods in this class and the clickactions queue

# When using write (cv2.setMouseCallback("IMAGE_NAME", cropper.click_and_crop)) and whenever they click the image
# it will call either standard_click or click_and_crop


# To get the position of the clicks call get and it will return the points
class ClickHandler:
    clickActions = Queue()

    def get(self):
        return self.clickActions.get()

    def clear(self):
        for i in range(self.clickActions.qsize()):
            self.clickActions.get()

    def size(self):
        return self.clickActions.qsize()

    def click_and_crop(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.clickActions.put((x, y))

        elif event == cv2.EVENT_LBUTTONUP:
            self.clickActions.put((x, y))

    def standard_click(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.clickActions.put((x, y))
