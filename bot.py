from ast import Try
import json
from operator import indexOf
from cv2 import getBuildInformation
from pyautogui import *
import pyautogui
import time
import keyboard
import win32api
import win32con
from util.rng import *
from Gui import *
from PIL import Image

# Settings
launcher_width = 1280
game_width = 1920
language = "spanish"
width = 320
height = 150
offset_x = 80
offset_y = 115
image_accuracy = 0.8
launcher_proportions = {"width": 51.3,
                        "height": 28.75, "width_pixels": launcher_width}
game_proportions = {"width": 76.8, "height": 43.2, "width_pixels": game_width}

settingsObj = {
    'language': "spanish",
    'image_accuracy': 0.8
}

pyautogui.FAILSAFE = False
translation_file = open("translation.json")
translated = json.load(translation_file)

targets_file = open("targets.json")
targets = json.load(targets_file)

launcher_title = translated[language]['launcher_title']
game_title = translated[language]['game_title']

# Information


# Targets
# Raw numbers are fractional numbers related to either the width or height of the LoL Launcher
# Check guide.jpg & guide.clip for reference.


# GUI
app = QApplication(sys.argv)
gui = Gui()
gui.show()

try:
    sys.exit(app.exec_())
except SystemExit:
    print("Closing guibot...")


def click(x, y, sleepTime=0.01):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(sleepTime)  # Pauses the script for 0.01 seconds.
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def right_click(x, y, sleepTime=0.01):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(sleepTime)  # Pauses the script for 0.01 seconds.
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)


def press_key(key_name):
    keyboard.press(key_name)
    time.sleep(random.randint(1, 10) / 100)
    keyboard.release(key_name)


def attackWalk(x, y, sleepTime=0.06):
    keyboard.press('a')
    time.sleep(random.randint(1, 10) / 100)
    keyboard.release('a')
    time.sleep(0.06)
    click(x, y, sleepTime)


def getWindowObj(title):
    if len(pyautogui.getWindowsWithTitle(title)) > 0:
        return pyautogui.getWindowsWithTitle(title)[0]
    else:
        return None


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

    def rightClickAt(self, x_fr, y_fr, proportions=game_proportions):
        x = int(self.x + (x_fr / proportions['width']) * self.width)
        y = int(self.y + (y_fr / proportions['height']) * self.height)

        right_click(x, y, random.randint(1, 10) / 100)

    def clickAt(self, x_fr, y_fr, proportions=game_proportions):
        x = int(self.x + (x_fr / proportions['width']) * self.width)
        y = int(self.y + (y_fr / proportions['height']) * self.height)

        click(x, y, random.randint(1, 10) / 100)

    def click(self, dx, dy, window_name):
        w = launcher_proportions["width"]
        h = launcher_proportions["height"]
        if window_name == 'game':
            w = game_proportions["width"]
            h = game_proportions["height"]

        click(self.x + int((dx / w) * self.width),
              (self.y + int((dy/h) * self.height)))

    # Search for target & wait until it is found
    def searchAndClickUntilFound(self, target, window_width, wait=0.0, language_independent=False, window_name="launcher", window_title=launcher_title, interruptor=None, limit=-1):
        time.sleep(wait)
        self.setFocusRegionsFromStore(target, window_name)

        clicked = False
        stop = False
        count = 0
        while not clicked and not stop:
            print('Searching... ', self.title, self.focus_region)
            clicked = self.searchAndClick(
                target, window_width, language_independent, click, window_title)

            if interruptor == 'game' and gameIsRunning():
                break

            if limit > 0:
                count += 1
                if count >= limit:
                    stop = True

    def searchAndRightClickUntilFound(self, target, window_width, wait=0.0, language_independent=False, window_name="launcher", window_title=launcher_title, limit=-1):
        time.sleep(wait)
        self.setFocusRegionsFromStore(target, window_name)

        clicked = False
        stop = False
        count = 0
        while not clicked and not stop:
            clicked = self.searchAndClick(
                target, window_width, language_independent, right_click, window_title)

            if limit > 0:
                count += 1
                if count >= limit:
                    stop = True

    # Search target & click on it if found

    def searchAndClickOnce(self, target, window_width, wait=0.0, language_independent=False, window_name="launcher", window_title=launcher_title):
        time.sleep(wait)
        self.setFocusRegionsFromStore(target, window_name)
        self.searchAndClick(target, window_width,
                            language_independent, click, window_title)

    def searchAndRightClickOnce(self, target, window_width, wait=0.0, language_independent=False, window_name="launcher", window_title=launcher_title):
        time.sleep(wait)
        self.setFocusRegionsFromStore(target, window_name)
        self.searchAndClick(target, window_width,
                            language_independent, rightClick, window_title)

    def search(self, target, window_width, language_independent=False, window_name="launcher", window_title=launcher_title):
        self.focusWindow(window_title)

        image_path = f"resources/{language}/{target}{window_width}.png"
        if language_independent:
            image_path = f"resources/{target}{window_width}.png"

        # Target found box
        return pyautogui.locateOnScreen(
            image_path, region=self.getFocusRegionsFromStore(target, window_name), confidence=image_accuracy)

    # OHS
    # def search(self, target, language_independent=False, window_name="launcher", window_title=launcher_title):
    #     self.focusWindow(window_title)

    #     image_path = f"resources/{language}/{target}.png"
    #     if language_independent:
    #         image_path = f"resources/{target}.png"

    #     # Target found box
    #     return pyautogui.locateOnScreen(
    #         image_path, region=self.getFocusRegionsFromStore(target, window_name), confidence=image_accuracy)

    ##

    def getCoordsFromTarget(self, target, proportions=game_proportions):
        x = int(self.x + (targets[target]['x'] /
                proportions['width']) * self.width)
        y = int(self.y + (targets[target]['y'] /
                proportions['height']) * self.height)
        return (x, y)

    def focusWindow(self, window_title):
        # Focus window
        windowObj = getWindowObj(window_title)
        while windowObj == None:
            time.sleep(0.05)
            print('looking for window', getWindowObj(window_title))
            windowObj = getWindowObj(window_title)
        windowObj.activate()

        # Update current window position ( In case the window is moving )
        self.setWindow(windowObj)

    def clickOn(self, x_fr, y_fr, window_title=launcher_title, sleepTime=0.15, click_func=click):
        self.moveCursorTo(x_fr, y_fr, window_title, sleepTime)
        click_func(x_fr, y_fr)

# pyautogui.displayMousePosition()


class LoLBot(Bot):
    def __init__(self):
        super().__init__()
        self.game_window = {}  # <left, top, width, height, title>
        self.launcher_window = {}
        self.status = 'Initializing'
        self.launcher_proportions = {"width": 51.3,
                                     "height": 28.75}
        self.game_proportions = {"width": 76.8, "height": 43.2}
        self.image_accuracy = 0.8
        self.language = 'spanish'
        self.launcher_title = 'League of Legends'
        self.game_title = 'League of Legends (TM) Client'

    def loadSettings(self, settingsObj):
        translation_file = open("translation.json")
        translated = json.load(translation_file)
        targets_file = open("targets.json")
        targets = json.load(targets_file)

        self.image_accuracy = settingsObj['image_accuracy']
        self.language = settingsObj['language']
        self.launcher_title = translated[self.language]['launcher_title']
        self.game_title = translated[self.language]['game_title']
        self.loadFocusRegions(targets)

    def getActiveWindows(self):
        self.launcher_window = getWindowObj(self.launcher_title)
        self.game_window = getWindowObj(self.launcher_title)

    def getLauncherWindow(self):
        self.launcher_window = getWindowObj(self.launcher_title)

    def getGameWindow(self):
        self.game_window = getWindowObj(self.launcher_title)

    def getTarget(self, target, language_independent=False, type="launcher", region=None):
        window_width = self.launcher_window.width
        if type == 'launcher':
            self.focusWindow(launcher_title)
        elif type == 'game':
            window_width = self.game_window.width
            self.focusWindow(game_title)

        image_path = f"resources/{self.language}/{target}{window_width}.png"
        if language_independent:
            image_path = f"resources/{target}{window_width}.png"

        # Target found box
        focus_region = self.getFocusRegionFromStore(target, type)
        if region != None:
            focus_region = region
        return pyautogui.locateOnScreen(
            image_path, region=focus_region, confidence=image_accuracy)

    def getFocusRegionFromStore(self, region_name, type="launcher"):
        w_fr = self.launcher_proportions["width"]
        h_fr = self.launcher_proportions["height"]
        w = self.launcher_window.width
        h = self.launcher_window.height
        if type == 'game':
            w_fr = self.game_proportions["width"]
            h_fr = self.game_proportions["height"]
            w = self.game_window.width
            h = self.game_window.height

        region_x = int(
            (self.stored_regions[region_name]['x'] / w_fr) * w)
        region_y = int(
            (self.stored_regions[region_name]['y'] / h_fr) * h)
        search_width = int(
            (self.stored_regions[region_name]['search_width'] / w_fr) * w)
        search_height = int(
            (self.stored_regions[region_name]['search_height'] / h_fr) * h)

        return (self.x + region_x, self.y + region_y, search_width, search_height)

    def getFocusRegionsFromStore(self, target_name, type="launcher"):
        w = launcher_proportions["width"]
        h = launcher_proportions["height"]
        if type == 'game':
            w = game_proportions["width"]
            h = game_proportions["height"]

        region_x = int(
            (self.stored_regions[target_name]['x'] / w) * self.width)
        region_y = int(
            (self.stored_regions[target_name]['y'] / h) * self.height)
        search_width = int(
            (self.stored_regions[target_name]['search_width'] / w) * self.width)
        search_height = int(
            (self.stored_regions[target_name]['search_height'] / h) * self.height)

        return (self.x + region_x, self.y + region_y, search_width, search_height)

    def searchAndClickUntilFound(self, target_name, type, click_func, wait=0.0, language_independent=False, limit=-1):
        time.sleep(wait)

        clicked = False
        stop = False
        count = 0
        while not clicked and not stop:
            print('Searching... ', self.title, self.focus_region)
            clicked = self.searchAndClick(
                target_name, type, language_independent, click_func)

            if limit > 0:
                count += 1
                if count >= limit:
                    stop = True

    def searchAndClick(self, target_name, type, language_independent, click_func):

        self.focusWindow(self.launcher_title)
        window_width = self.launcher_window.width
        if type == 'game':
            self.focusWindow(self.game_title)
            window_width = self.game_window.width

        image_path = f"resources/{self.language}/{target_name}{window_width}.png"
        if language_independent:
            image_path = f"resources/{target_name}{window_width}.png"

        # Target found box
        on_view_location = pyautogui.locateOnScreen(
            image_path, region=self.getFocusRegionsFromStore(target_name, type), confidence=image_accuracy)

        if on_view_location != None:
            print(f"Target {target_name} found")
            with Image.open(image_path) as img:
                # Click on the center of the target
                click_func(int(on_view_location[0] + img.size[0] / 2),
                           int(on_view_location[1] + img.size[1] / 2))

            return True
        else:
            print(f"{target_name} not found...")

        time.sleep(0.4)
        return False

    def getDimensionFromFractions(self, x_fr, y_fr, proportions, float=False):
        x = self.x + (x_fr / proportions['width']) * self.width
        y = self.y + (y_fr / proportions['height']) * self.height

        if float:
            return (x, y)
        return (int(x), int(y))

    def getProportionFromTitle(self, window_title):
        if window_title == self.launcher_title:
            return self.launcher_proportions
        elif window_title == self.game_title:
            return self.game_proportions

    def getCoordsByTarget(self, target_name, type):
        cur_x = self.launcher_window.x
        cur_y = self.launcher_window.y
        cur_width = self.launcher_window.width
        cur_height = self.launcher_window.height
        width_proportion = self.launcher_proportions['width']
        height_proportion = self.launcher_proportions['height']
        if type == 'game':
            cur_x = self.game_window.x
            cur_y = self.game_window.y
            cur_width = self.game_window.width
            cur_height = self.game_window.height
            width_proportion = self.game_proportions['width']
            height_proportion = self.game_proportions['height']

        return (int(cur_x + (self.stored_regions[target_name]['x'] /
                width_proportion) * cur_width), int(cur_y + (self.stored_regions[target_name]['y'] /
                                                             height_proportion) * cur_height))

    def moveCursorTo(self, x_fr, y_fr, window_title=launcher_title, sleepTime=0.15):
        self.focusWindow(window_title)

        win32api.SetCursorPos(self.getDimensionFromFractions(
            x_fr, y_fr, self.getProportionFromTitle(window_title)))
        time.sleep(sleepTime)

    def clickAt(self, x_fr, y_fr, proportions=game_proportions):
        x = int(self.x + (x_fr / proportions['width']) * self.width)
        y = int(self.y + (y_fr / proportions['height']) * self.height)

        click(x, y, random.randint(1, 10) / 100)

    def attackWalkRandomCoord(self):
        x = self.game_window.x + random.randint(0, self.game_window.width - 1)
        y = self.game_window.y + random.randint(0, self.game_window.height - 1)

        attackWalk(x, y)

    def findMatchFromLauncher(self):
        try:
            find_match = ['play', 'ai', 'intermedia', 'confirm',
                          'findMatch', 'accept', 'pickChamp', 'lockChamp']
            game_has_started = False

            while not game_has_started:
                time.sleep(0.6)

                # Click on buttons
                for target_name in find_match:

                    # Enters champioon select
                    if target_name == 'pickChamp':
                        time.sleep(10)
                        print("Picking champion...")
                        for n in range(5):
                            self.click(
                                self.stored_regions['pickChamp']['x'] + n * self.stored_regions['pickChamp']['x_gap'], self.stored_regions['pickChamp']['y'], 'launcher')
                            time.sleep(0.2)
                    else:
                        print(f"Looking for target {target_name}...")
                        target = self.getTarget(target_name)
                        if target != None:
                            print(f"Target {target} found")
                            with Image.open(f"resources/{language}/{target_name}{self.launcher_window.width}.png") as img:

                                # Click on the center of the target
                                click(int(target[0] + img.size[0] / 2),
                                      int(target[1] + img.size[1] / 2))
                        else:
                            print(f"{target_name} not found.")

                        time.sleep(0.6)

                windows = pyautogui.getWindowsWithTitle(self.game_title)
                if len(windows) > 0:
                    game_has_started = True
        except:
            self.findMatchFromLauncher()

    def waitGameToLaunch(self):
        game_running = False
        while not game_running:
            print('Waiting for game to start...')
            windows = pyautogui.getWindowsWithTitle(self.game_title)
            if len(windows) > 0:
                print('Game has started.')
                self.setWindow(windows[0])
                self.getGameWindow()
                time.sleep(20)
                game_running = True

    def playGame(self):
        def buy(item_name):
            press_key('p')

            time.sleep(2)
            if self.getTarget('searchShopItem', type='game') != None:
                self.searchAndClickUntilFound(
                    'searchShopItem', 'game', click, limit=4)
                typewrite(self.stored_regions[item_name]['search_term'])
                time.sleep(0.5)
                self.searchAndClickUntilFound(
                    item_name, 'game', right_click, limit=4)

                time.sleep(0.4)
                if self.getTarget('redo', type='game') != None:
                    press_key('p')
                    return True
            press_key('p')
            return False

        # Game in progress
        buy_count = 0
        items_to_buy = ['doranSword', 'krakenSlayer', 'hydra']
        game_in_progress = True
        lane_to_go = random.randint(1, 3)
        aggresive_pushing = False
        seconds = 0
        while self.getTarget('continue') == None and game_in_progress:

            if len(pyautogui.getWindowsWithTitle(game_title)) > 0:
                # Check health
                low_health_point = self.getCoordsByTarget('lowHp', 'game')
                if pyautogui.pixelMatchesColor(low_health_point[0], low_health_point[1], expectedRGBColor=(1, 13, 7), tolerance=12):
                    print('player is low health! Walking to fountain...')

                    # Walk to fountain
                    fountain = self.getCoordsByTarget('fountain', 'game')
                    right_click(fountain[0], fountain[1])
                    time.sleep(10)

                    # Buy something from shop
                    if buy_count < len(items_to_buy):
                        print(
                            f'Trying to purchase {items_to_buy[buy_count]}...')
                        if buy(items_to_buy[buy_count]):
                            buy_count += 1

                    # Set new lane to go
                    lane_to_go = random.randint(1, 3)

                # Attack forward (Top, Mid, Bot)
                if aggresive_pushing:
                    nexus = self.getCoordsByTarget('nexus')
                    attackWalk(nexus[0], nexus[1])
                elif lane_to_go == 1:
                    topA = self.getCoordsByTarget('topA')
                    attackWalk(topA[0], topA[1])
                elif lane_to_go == 2:
                    midA = self.getCoordsByTarget('midA')
                    attackWalk(midA[0], midA[1])
                elif lane_to_go == 3:
                    botA = self.getCoordsByTarget('botA')
                    attackWalk(botA[0], botA[1])

                # Miscellaneous Periodic checks
                if seconds % 6 == 0:
                    # Update current window position ( In case the window is moving )
                    self.focusWindow(self.game_title)

                    # Lock camera
                    unlock_icon = self.getTarget(
                        'unlockedCamera', language_independent=True, type='game')
                    if unlock_icon != None:
                        press_key('y')

                    # Attack-walk to random coord
                    self.attackWalkRandomCoord()

                    # Close store if open
                    close_button = self.getTarget(
                        'close', language_independent=True, type='game')
                    if close_button != None:
                        press_key('p')

                if seconds % 10 == 0:
                    # Use random skill
                    skills = ['q', 'w', 'e', 'r', 'd', 'f']
                    for i in range(random.randint(1, 6)):
                        press_key(skills[random.randint(0, 5)])
                        time.sleep(0.05)

                        w = self.game_proportions["width"]
                        h = self.game_proportions["height"]
                        x_fr = random.randint(
                            self.stored_regions['closeRange']['x_start'], self.stored_regions['closeRange']['x_end'])
                        y_fr = random.randint(
                            self.stored_regions['closeRange']['y_start'], self.stored_regions['closeRange']['y_end'])

                        click(self.game_window.x + int((x_fr / w) * self.game_window.width),
                              (self.game_window.y + int((y_fr / h) * self.game_window.height)))
                        time.sleep(random.random())

                    # Skills up
                    if self.getTarget('skillUp', language_independent=True, type='game'):
                        self.searchAndClick(
                            'skillUp', 'game', True, click)

                # Every 1:30 minute, trigger between defensive and aggresive pushing
                if seconds % 90 == 0 and seconds != 0:
                    aggresive_pushing = not aggresive_pushing

                    fountain = self.getCoordsByTarget('fountain')
                    right_click(fountain[0], fountain[1])
                    # Wait for hp to get full
                    time.sleep(10)

                    # Buy something from shop
                    buy('krakenSlayer')

                if seconds % 285 == 0:
                    fountain = self.getCoordsByTarget('fountain')
                    right_click(fountain[0], fountain[1])
                    # Wait for hp to get full
                    time.sleep(10)

                    # Buy something from shop
                    buy('hydra')

                # 10% chance to move back a little
                if random.randint(1, 10) == 1:
                    fountain = self.getCoordsByTarget('fountain')
                    right_click(fountain[0], fountain[1])

                time.sleep(1)

                def aggresivePushing():
                    if aggresive_pushing:
                        return ' aggresively.'
                    else:
                        return '.'
                print('Time: ', seconds, 's. Pushing lane: ', [
                      'top', 'mid', 'bot'][lane_to_go], aggresivePushing())
                seconds += 1

            else:
                time.sleep(32)
                if len(pyautogui.getWindowsWithTitle(game_title)) <= 0:
                    game_in_progress = False

        # Game is over
        continue_button = self.getTarget('continue')
        if continue_button != None:
            with Image.open(f"resources/{self.language}/continue{self.game_window.width}.png") as img:
                # Click on the center of the target
                click(int(continue_button[0] + img.size[0] / 2),
                      int(continue_button[1] + img.size[1] / 2))
                # Press Enter in case click fails
                press_key('enter')

    def postGame(self):
        # Focus launcher
        self.focusWindow(self.launcher_title)

        time.sleep(10)
        # honor opponents
        click(int(self.launcher_window.width / 2),
              (int(self.launcher_window.height / 2)))

        # accept gifts & level ups
        launcher_region = (self.launcher_window.x, self.launcher_window.y,
                           self.launcher_window.width, self.launcher_window.height)

        play_again_button = self.getTarget('playAgain')
        while play_again_button == None:
            time.sleep(4)

            # Look if a free champion is given
            for champ in self.stored_regions['championsPosition']:
                champ_box = self.getTarget(
                    champ['name'], language_independent=True)

                if champ_box != None:
                    champ_box_width = self.launcher_window.width / \
                        champ['out_of']
                    x_fr = (champ_box_width *
                            champ['position']) - champ_box_width / 2
                    y_fr = self.stored_regions['hoverSelect']['y']

                    self.moveCursorTo(x_fr, y_fr, self.game_title)
                    time.sleep(3)
                    click(x_fr, y_fr)
                    break

            # Press OK Button on screen
            accept_levelup_button = self.getTarget(
                'ok', type='launcher', region=launcher_region)
            # accept_gifts_button = getButtonLauncher('acceptGifts', launcher_region)

            if accept_levelup_button != None:
                with Image.open(f"resources/{self.language}/ok{self.launcher_window.width}.png") as img:

                    click(int(accept_levelup_button[0] + img.size[0] / 2),
                          int(accept_levelup_button[1] + img.size[1] / 2))
                time.sleep(2)

            play_again_button = self.getTarget(
                'playAgain', type='launcher', region=launcher_region)


# Click Flows:
find_match = ['play', 'ai', 'intermedia', 'confirm',
              'findMatch', 'accept', 'pickChamp', 'lockChamp']
find_match_again = ['playAgain', 'findMatch',
                    'accept', 'pickChamp', 'lockChamp']
random_clicks = ['randomClick']

# Game Flows
blind_play = {
    "actions": ['fountain_to_top', 'fountain_to_mid', 'fountain_to_bot', 'random_attack', 'push_top', 'push_mid', 'push_bot', "farm_camps", "buy_random_item", "buy_ad_items", "unsafeWalk_to_", "safeWalk_to" "random_ward", "ward_specific_point", "random_ward_on_darkness", "upgrade_skill", "use_skill", "toggle_skill"],
    "params": {"random_delays": True, },
    "intentions": ["hide", "defend_self", "defend_structure", "defend_ally", "sneak_to", "kite", "farm", "kill", "kill_1for1", "kill_without_dying", "go_to_safety", "heal"],
    "state": ["attacking_target", "holding", "attacking_area", "walking", "attack_walk", "hidden", "healing", "immortal", "tougher"]
}

# Cycle 1


# - Find Match

# Setup
currentWindow = LoLBot()
currentWindow.setWindow(getWindowObj(launcher_title))
currentWindow.loadSettings(settingsObj)
currentWindow.getActiveWindows()


def exitNotPressed():
    return not (keyboard.is_pressed('ctrl+escape') or keyboard.is_pressed('ctrl+shift+q'))


def getButton(target, window_title=game_title, language_independent=False, confidence=image_accuracy):
    windows = pyautogui.getWindowsWithTitle(window_title)

    def imagePath():
        if language_independent:
            return f"resources/{target}{game_width}.png"
        else:
            return f"resources/{language}/{target}{game_width}.png"

    if len(windows) > 0:
        currentWindow.setWindow(windows[0])
        currentWindow.setFocusRegionsFromStore(
            region_name=target, window_name="game")
        print('Locating --> ', target, pyautogui.locateOnScreen(
            imagePath(), region=currentWindow.getFocusRegionsFromStore(region_name=target, window_name="game"), confidence=confidence))
        return pyautogui.locateOnScreen(imagePath(), region=currentWindow.getFocusRegionsFromStore(region_name=target, window_name="game"), confidence=confidence)
    return None


def getButtonNew(target, window_title=game_title, language_independent=False):
    windows = pyautogui.getWindowsWithTitle(window_title)

    def windowWidth():
        if window_title == game_title:
            return game_width
        elif window_title == launcher_title:
            return launcher_width
        else:
            return '1280'

    def imagePath():
        if language_independent:
            return f"resources/{target}{windowWidth()}.png"
        else:
            return f"resources/{language}/{target}{windowWidth()}.png"

    if len(windows) > 0:
        currentWindow.setWindow(windows[0])
        print('Locating --> ', target, pyautogui.locateOnScreen(
            imagePath(), region=currentWindow.region, confidence=image_accuracy))
        return pyautogui.locateOnScreen(imagePath(), region=currentWindow.region, confidence=image_accuracy)
    return None


def getButtonLauncher(target, region):
    print('Locating --> ', target, pyautogui.locateOnScreen(
        f"resources/{language}/{target}{launcher_width}.png", region=region, confidence=image_accuracy))
    return pyautogui.locateOnScreen(f"resources/{language}/{target}{launcher_width}.png", region=region, confidence=image_accuracy)


# Process
def findMatchFromLauncher():
    target_index = 0
    game_has_started = False
    while exitNotPressed() and not game_has_started:
        def acceptButtonOnSight():
            launcher_region = (currentWindow.x, currentWindow.y,
                               currentWindow.width, currentWindow.height)
            accept_button = getButtonLauncher('accept', launcher_region)
            if accept_button == None:
                return False
            return True

        time.sleep(0.6)  # <--- CHECAR ESTO LUEGO

        # Picking champion
        if target_index < len(find_match):
            if find_match[target_index] == 'pickChamp':
                time.sleep(15)
                print("Picking champion...")
                for n in range(5):
                    currentWindow.click(
                        targets['pickChamp']['x'] + n * targets['pickChamp']['x_gap'], targets['pickChamp']['y'])
                    time.sleep(0.2)
            else:
                # Check if match was rejected
                if acceptButtonOnSight():
                    target_index = find_match.index('accept')

                def interruptor():
                    print('interruptor: ', acceptButtonOnSight())
                    return not acceptButtonOnSight()

                limit = -1
                if find_match[target_index] == 'lockChamp':
                    limit = 90

                print(find_match[target_index])
                currentWindow.searchAndClickUntilFound(
                    find_match[target_index], launcher_width, limit=limit)
        else:
            # Check if match was rejected
            if acceptButtonOnSight():
                target_index = find_match.index('accept')

        target_index += 1

        windows = pyautogui.getWindowsWithTitle(game_title)
        if len(windows) > 0:
            game_has_started = True


def waitGameToLaunch():
    # Wait for game to launch
    game_running = False
    while exitNotPressed() and not game_running:
        windows = pyautogui.getWindowsWithTitle(game_title)
        if len(windows) > 0:
            currentWindow.setWindow(windows[0])
            time.sleep(20)
            game_running = True


def gameIsRunning():
    windows = pyautogui.getWindowsWithTitle(game_title)
    if len(windows) > 0:
        return True
    return False


def blindClickGame():
    def buy(item_name):
        press_key('p')

        time.sleep(2)
        if getButtonNew('searchShopItem') != None:
            currentWindow.searchAndClickUntilFound(
                'searchShopItem', window_width=game_width, window_name='game', window_title=game_title, limit=4)
            typewrite(targets[item_name]['search_term'])
            time.sleep(0.5)
            currentWindow.searchAndRightClickUntilFound(
                item_name, window_width=game_width, window_name='game', window_title=game_title, limit=4)

            time.sleep(0.4)
            if getButtonNew('redo') != None:
                press_key('p')
                return True
        press_key('p')
        return False

    # Game in progress
    buy_count = 0
    items_to_buy = ['doranSword', 'krakenSlayer', 'hydra']
    game_in_progress = True
    lane_to_go = random.randint(1, 3)
    aggresive_pushing = False
    seconds = 0
    while exitNotPressed() and getButton('continue') == None and game_in_progress:

        if len(pyautogui.getWindowsWithTitle(game_title)) > 0:
            # Check health
            low_health_point = currentWindow.getCoordsFromTarget('lowHp')
            print(low_health_point)
            if pyautogui.pixelMatchesColor(low_health_point[0], low_health_point[1], expectedRGBColor=(1, 13, 7), tolerance=12):
                print('player is low health!')
                cur_time = 0
                time_limit = 50

                # Walk to fountain
                fountain = currentWindow.getCoordsFromTarget('fountain')
                currentWindow.clickAt(fountain[0], fountain[1])

                # Wait for hp to get full
                full_hp = getButton('fullHp', language_independent=True)
                while full_hp == None:
                    print('Waiting for hp to recover...')
                    time.sleep(2)
                    currentWindow.clickAt(fountain[0], fountain[1])
                    cur_time += 2

                    if cur_time >= time_limit:
                        break

                # Buy something from shop
                if buy_count < len(items_to_buy):
                    if buy(items_to_buy[buy_count]):
                        buy_count += 1

                # Set new lane to go
                lane_to_go = random.randint(1, 3)

            # Attack forward (Top, Mid, Bot)
            if aggresive_pushing:
                nexus = currentWindow.getCoordsFromTarget('nexus')
                attackWalk(nexus[0], nexus[1])
            elif lane_to_go == 1:
                topA = currentWindow.getCoordsFromTarget('topA')
                attackWalk(topA[0], topA[1])
            elif lane_to_go == 2:
                midA = currentWindow.getCoordsFromTarget('midA')
                attackWalk(midA[0], midA[1])
            elif lane_to_go == 3:
                botA = currentWindow.getCoordsFromTarget('botA')
                attackWalk(botA[0], botA[1])

            # Miscellaneous Periodic checks
            if seconds % 6 == 0:
                # Update current window position ( In case the window is moving )
                game = getWindowObj(currentWindow.title)
                currentWindow.setWindow(game)

                # Lock camera
                unlock_icon = getButton(
                    'unlockedCamera', language_independent=True, confidence=0.98)
                if unlock_icon != None:
                    press_key('y')

                # Attack-walk to random coord
                currentWindow.attackWalkRandomCoord()

                # Close store if open
                close_button = getButton('close', language_independent=True)
                if close_button != None:
                    press_key('p')

            if seconds % 10 == 0:
                # Use random skill
                skills = ['q', 'w', 'e', 'r', 'd', 'f']
                for i in range(random.randint(1, 6)):
                    press_key(skills[random.randint(0, 5)])
                    time.sleep(0.05)

                    w = game_proportions["width"]
                    h = game_proportions["height"]
                    x_fr = random.randint(
                        targets['closeRange']['x_start'], targets['closeRange']['x_end'])
                    y_fr = random.randint(
                        targets['closeRange']['y_start'], targets['closeRange']['y_end'])

                    click(currentWindow.x + int((x_fr / w) * currentWindow.width),
                          (currentWindow.y + int((y_fr / h) * currentWindow.height)))
                    time.sleep(random.random())

            if seconds % 5 == 0:
                # Skills up
                if getButton('skillUp', language_independent=True):
                    currentWindow.searchAndClickOnce(
                        'skillUp', game_width, language_independent=True, window_name='game', window_title=game_title)

            # Every 1:30 minute, trigger between defensive and aggresive pushing
            if seconds % 90 == 0 and seconds != 0:
                aggresive_pushing = not aggresive_pushing

                # Temporary shopping
                # Walk to fountain
                fountain = currentWindow.getCoordsFromTarget('fountain')
                currentWindow.rightClickAt(fountain[0], fountain[1])
                # Wait for hp to get full
                time.sleep(30)

                # Buy something from shop
                buy('krakenSlayer')

            if seconds % 285 == 0:
                # Temporary shopping
                # Walk to fountain
                fountain = currentWindow.getCoordsFromTarget('fountain')
                currentWindow.rightClickAt(fountain[0], fountain[1])
                # Wait for hp to get full
                time.sleep(30)

                # Buy something from shop
                buy('hydra')

            # Move back a little
            if random.randint(1, 10) == 1:
                fountain = currentWindow.getCoordsFromTarget('fountain')
                currentWindow.clickAt(fountain[0], fountain[1])

            time.sleep(1)
            print('Time: ', seconds, 'Aggresive pushing: ',
                  aggresive_pushing, 'lane: ', lane_to_go)
            seconds += 1

        else:
            time.sleep(32)
            if len(pyautogui.getWindowsWithTitle(game_title)) <= 0:
                game_in_progress = False

    # Game is over
    continue_button = getButton('continue')
    if continue_button != None:
        with Image.open(f"resources/{language}/continue{game_width}.png") as img:

            # Click on the center of the target
            click(int(continue_button[0] + img.size[0] / 2),
                  int(continue_button[1] + img.size[1] / 2))
            # Press Enter in case click fails
            press_key('enter')


def postGame():
    # Focus launcher
    currentWindow.focusWindow(launcher_title)

    time.sleep(10)
    # honor opponents
    click(int(launcher_width / 2),
          (int(currentWindow.height / 2)))

    # accept gifts & level ups
    launcher_region = (currentWindow.x, currentWindow.y,
                       currentWindow.width, currentWindow.height)

    play_again_button = getButtonLauncher('playAgain', launcher_region)
    while play_again_button == None:
        time.sleep(4)

        currentWindow.setWindow(
            pyautogui.getWindowsWithTitle(launcher_title)[0])

        # Look if a free champion is given
        for champ in targets['championsPosition']:
            champ_box = getButtonNew(
                champ['name'], window_title=launcher_title, language_independent=True)

            if champ_box != None:
                champ_box_width = launcher_width / champ['out_of']
                x_fr = (champ_box_width *
                        champ['position']) - champ_box_width / 2
                y_fr = targets['hoverSelect']['y']

                currentWindow.moveCursorTo(x_fr, y_fr)
                time.sleep(3)
                click(x_fr, y_fr)
                break

        # Press OK Button on screen
        accept_levelup_button = getButtonLauncher('ok', launcher_region)
        # accept_gifts_button = getButtonLauncher('acceptGifts', launcher_region)

        if accept_levelup_button != None:
            with Image.open(f"resources/{language}/ok{launcher_width}.png") as img:

                click(int(accept_levelup_button[0] + img.size[0] / 2),
                      int(accept_levelup_button[1] + img.size[1] / 2))
            time.sleep(2)

        play_again_button = getButtonLauncher('playAgain', launcher_region)


def findMatchAgain():
    target_index = 0
    game_has_started = False
    while exitNotPressed() and not game_has_started:
        def acceptButtonOnSight():
            launcher_region = (currentWindow.x, currentWindow.y,
                               currentWindow.width, currentWindow.height)
            accept_button = getButtonLauncher('accept', launcher_region)
            if accept_button == None:
                return False
            return True

        time.sleep(0.6)  # <--- CHECAR ESTO LUEGO

        # Picking champion
        if target_index < len(find_match_again):
            if find_match_again[target_index] == 'pickChamp':
                time.sleep(15)
                print("Picking champion...")
                for n in range(5):
                    currentWindow.click(
                        targets['pickChamp']['x'] + n * targets['pickChamp']['x_gap'], targets['pickChamp']['y'])
                    time.sleep(0.2)
            else:
                # Check if match was rejected
                if acceptButtonOnSight():
                    target_index = find_match_again.index('accept')

                def interruptor():
                    print('interruptor: ', acceptButtonOnSight())
                    return not acceptButtonOnSight()

                limit = -1
                if find_match_again[target_index] == 'lockChamp':
                    limit = 90

                currentWindow.searchAndClickUntilFound(
                    find_match_again[target_index], launcher_width, limit=limit)
        else:
            # Check if match was rejected
            if acceptButtonOnSight():
                target_index = find_match_again.index('accept')

        target_index += 1

        windows = pyautogui.getWindowsWithTitle(game_title)
        if len(windows) > 0:
            game_has_started = True


def cycle_fromBeginning():
    currentWindow.findMatchFromLauncher()
    waitGameToLaunch()
    blindClickGame()
    postGame()

    while exitNotPressed():
        findMatchAgain()
        waitGameToLaunch()
        blindClickGame()
        postGame()


def cycle_fromGame():
    blindClickGame()
    postGame()

    while exitNotPressed():
        findMatchAgain()
        waitGameToLaunch()
        blindClickGame()
        postGame()


def cycle_fromAfterMatch():
    postGame()

    while exitNotPressed():
        findMatchAgain()
        waitGameToLaunch()
        blindClickGame()
        postGame()


def cycle_test():
    postGame()
    findMatchAgain()


# Main
cycle_fromBeginning()
# cycle_test()

# Watch health
# Watch dead status


# Accept if something is received

# snapshot = pyautogui.screenshot(
#     region=(self.x, self.y, buttonWidth, buttonHeight))
# snapshot.save(r"C:\guibot\play.png")

# Blind play

# Know what color of team is
# Watch if champion in fountain
# Watch health
# Watch dead status
# Watch if being targeted by turret
# Press Tab occasionally

# attack-walk to a line
# If health below 30% walk back
