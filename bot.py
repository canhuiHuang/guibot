from pyautogui import *
import pyautogui
from util.controls import *


class Bot:
    def __init__(self):
        self.title = ''
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.region = ()
        self.stored_regions = {}
        self.focus_region = ()
        self.gui = None

    def setWindow(self, windowObj):
        self.title = windowObj.title
        self.x = windowObj.left
        self.y = windowObj.top
        self.width = windowObj.width
        self.height = windowObj.height
        self.region = (windowObj.left, windowObj.top,
                       windowObj.width, windowObj.height)

    def loadFocusRegions(self, regions):
        self.stored_regions = regions

    def setFocusRegionsFromStore(self, region_name, window_name="launcher"):
        self.focus_region = self.getFocusRegionsFromStore(
            region_name, window_name)

    def setNewFocusRegion(self, regionObj):
        self.focus_region = regionObj

    def clickRandomCoord(self):
        x = self.x + random.randint(0, self.width - 1)
        y = self.y + random.randint(0, self.height - 1)

        click(x, y)

    def rightClickRandomCoord(self):
        x = self.x + random.randint(0, self.width - 1)
        y = self.y + random.randint(0, self.height - 1)

        right_click(x, y)


def exitNotPressed():
    return not (keyboard.is_pressed('ctrl+escape') or keyboard.is_pressed('ctrl+shift+q'))


def getWindowObj(title):
    if len(pyautogui.getWindowsWithTitle(title)) > 0:
        for window in pyautogui.getWindowsWithTitle(title):
            if window.title == title:
                return window
    return None
