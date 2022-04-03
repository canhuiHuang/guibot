import json
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
launcher_proportions = {"width": 51.3, "height": 28.75}
game_proportions = {"width": 76.8, "height": 43.2}

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


class WindowInstance:
    def __init__(self, windowObj):
        self.title = windowObj.title
        self.x = windowObj.left
        self.y = windowObj.top
        self.width = windowObj.width
        self.height = windowObj.height
        self.stored_regions = {}
        self.focus_region = ()

    def setWindow(self, windowObj):
        self.title = windowObj.title
        self.x = windowObj.left
        self.y = windowObj.top
        self.width = windowObj.width
        self.height = windowObj.height

    def loadFocusRegions(self, regions):
        self.stored_regions = regions

    def setFocusRegionsFromStore(self, region_name, window_name="launcher"):
        self.focus_region = self.getFocusRegionsFromStore(
            region_name, window_name)

    def getFocusRegionsFromStore(self, region_name, window_name="launcher"):
        w = launcher_proportions["width"]
        h = launcher_proportions["height"]
        if window_name == 'game':
            w = game_proportions["width"]
            h = game_proportions["height"]

        region_x = int(
            (self.stored_regions[region_name]['x'] / w) * self.width)
        region_y = int(
            (self.stored_regions[region_name]['y'] / h) * self.height)
        search_width = int(
            (self.stored_regions[region_name]['search_width'] / w) * self.width)
        search_height = int(
            (self.stored_regions[region_name]['search_height'] / h) * self.height)

        print('focus region: ', (self.x + region_x, self.y + region_y, search_width, search_height))
        return (self.x + region_x, self.y + region_y, search_width, search_height)

    def setNewFocusRegion(self, regionObj):
        self.focus_region = regionObj

    def clickRandomCoord(self):
        x = self.x + random.randint(0, self.width - 1)
        y = self.y + random.randint(0, self.height - 1)

        click(x, y)

    def rightClickRandomCoord(self):
        x = self.x + random.randint(0, self.width - 1)
        y = self.y + random.randint(0, self.height - 1)

        rightClick(x, y)

    def attackWalkRandomCoord(self):
        x = self.x + random.randint(0, self.width - 1)
        y = self.y + random.randint(0, self.height - 1)

        attackWalk(x, y)

    def click(self, dx, dy):
        w = launcher_proportions["width"]
        h = launcher_proportions["height"]

        click(self.x + int((dx / w) * self.width),
              (self.y + int((dy/h) * self.height)))

    # Search for target & wait until it is found
    def searchAndClickUntilFound(self, target, window_width, wait=0.0, language_independent=False, window_name="launcher", window_title = launcher_title):
        time.sleep(wait)
        self.setFocusRegionsFromStore(target, window_name)

        clicked = False
        while not clicked:
            print('wtf man', self.title, self.focus_region)
            clicked = self.searchAndClick(
                target, window_width, language_independent, click, window_title)

    def searchAndRightClickUntilFound(self, target, window_width, wait=0.0, language_independent=False, window_name="launcher", window_title = launcher_title):
        time.sleep(wait)
        self.setFocusRegionsFromStore(target, window_name)

        clicked = False
        while not clicked:
            clicked = self.searchAndClick(
                target, window_width, language_independent, rightClick, window_title)

    # Search target & click on it if found
    def searchAndClickOnce(self, target, window_width, wait=0.0, language_independent=False, window_name="launcher", window_title = launcher_title):
        time.sleep(wait)
        self.setFocusRegionsFromStore(target, window_name)
        self.searchAndClick(target, window_width, language_independent, click, window_title)

    def searchAndRightClickOnce(self, target, window_width, wait=0.0, language_independent=False, window_name="launcher", window_title = launcher_title):
        time.sleep(wait)
        self.setFocusRegionsFromStore(target, window_name)
        self.searchAndClick(target, window_width,
                            language_independent, rightClick, window_title)

    def searchAndClick(self, target, window_width, language_independent, click_func, window_title = launcher_title):
        # Focus window
        launcher = getWindowObj(window_title)
        while launcher == None:
            print('looking for launcher', getWindowObj(window_title))
            launcher = getWindowObj(window_title)
        launcher.activate()

        # Update current window position ( In case the window is moving )
        self.setWindow(launcher)

        # Look for the target button? & click it
        if language_independent:
            image_path = f"resources/{target}{window_width}.png"
        else:
            image_path = f"resources/{language}/{target}{window_width}.png"

        # Target found box
        on_view_location = pyautogui.locateOnScreen(
            image_path, region=self.focus_region, confidence=image_accuracy)

        if on_view_location != None:
            print(f"Target {target} found")
            with Image.open(image_path) as img:
                # on_view_location[0] --> target_found_box x coord
                # on_view_location[1] --> target_found_box y coord

                # Click on the center of the target
                click_func(int(on_view_location[0] + img.size[0] / 2),
                           int(on_view_location[1] + img.size[1] / 2))

            time.sleep(0.4)
            return True
        else:
            print(f"{target} not found...")
            time.sleep(0.4)
        return False

# pyautogui.displayMousePosition()


def getWindowObj(title):
    if len(pyautogui.getWindowsWithTitle(title)) > 0:
        return pyautogui.getWindowsWithTitle(title)[0]
    else:
        return None


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
currentWindow = WindowInstance(getWindowObj(launcher_title))
currentWindow.loadFocusRegions(targets)

def exitNotPressed():
    return not (keyboard.is_pressed('ctrl+escape') or keyboard.is_pressed('ctrl+shift+q'))


def getButton(target):
    game_Windows = pyautogui.getWindowsWithTitle(
        translated[language]['game_title'])

    if len(game_Windows) > 0:
        currentWindow.setWindow(game_Windows[0])
        currentWindow.setFocusRegionsFromStore(
            region_name='continue', window_name="game")
        print(target, pyautogui.locateOnScreen(
            f"resources/{language}/{target}{game_width}.png", region=currentWindow.getFocusRegionsFromStore(region_name='continue', window_name="game"), confidence=image_accuracy))
        return pyautogui.locateOnScreen(f"resources/{language}/{target}{game_width}.png", region=currentWindow.getFocusRegionsFromStore(region_name='continue', window_name="game"), confidence=image_accuracy)
    return None


def getButtonLauncher(target, region):
    currentWindow.setFocusRegionsFromStore(
        region_name='continue', window_name="launcher")

    print(target, pyautogui.locateOnScreen(
        f"resources/{language}/{target}{launcher_width}.png", region=region, confidence=image_accuracy))
    return pyautogui.locateOnScreen(f"resources/{language}/{target}{launcher_width}.png", region=region, confidence=image_accuracy)


# Process
def findMatchFromLauncher():
    target_index = 0
    while exitNotPressed() and target_index < len(find_match):
        if find_match[target_index] == 'pickChamp':
            time.sleep(15)  # <--- CHECAR ESTO LUEGO

            # Check if match was rejected
            launcher_region = (currentWindow.x, currentWindow.y,
                            currentWindow.width, currentWindow.height)
            accept_button = getButtonLauncher('accept', launcher_region)
            # Check if champ select, if so, pick champ, else target_index -= 1

            if accept_button == None:
                print("Picking champion...")
                for n in range(5):
                    currentWindow.click(
                        targets['pickChamp']['x'] + n * targets['pickChamp']['x_gap'], targets['pickChamp']['y'])
                    time.sleep(0.4)
                target_index += 1
            else:
                target_index -= 1

        else:
            currentWindow.searchAndClickUntilFound(
                find_match[target_index], launcher_width)
            target_index += 1

def waitGameToLaunch(): 
    # Wait for game to launch
    game_running = False
    while exitNotPressed() and not game_running:
        windows = pyautogui.getWindowsWithTitle(game_title)
        if len(windows) > 0:
            currentWindow.setWindow(windows[0])
            time.sleep(20)
            game_running = True

def blindClickGame():
    # Game in progress
    while exitNotPressed() and getButton('continue') == None:

        if len(pyautogui.getWindowsWithTitle(game_title)) > 0:
            # Update current window position ( In case the window is moving )
            game = getWindowObj(currentWindow.title)

            # Attack-walk to random coord
            currentWindow.setWindow(game)
            currentWindow.attackWalkRandomCoord()

            # Close store if open
            close_button = getButton('close')
            if close_button != None:
                press_key('p')
            # currentWindow.searchAndClickOnce(
            #     'close', game_width, language_independent=True, window_name="game", window_title="launcher_title")

            time.sleep(8)

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
    currentWindow.setWindow(pyautogui.getWindowsWithTitle(launcher_title)[0])

    time.sleep(10)
    # honor opponents
    click(int(launcher_width / 2),
        (int(currentWindow.height / 2)))

    # accept gifts
    # level ups
    launcher_region = (currentWindow.x, currentWindow.y,
                    currentWindow.width, currentWindow.height)

    play_again_button = getButtonLauncher('playAgain', launcher_region)
    while play_again_button == None:
        currentWindow.setWindow(pyautogui.getWindowsWithTitle(launcher_title)[0])

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
    while exitNotPressed() and target_index < len(find_match_again):
        currentWindow.setWindow(pyautogui.getWindowsWithTitle(launcher_title)[0])

        print('Current: ', find_match_again[target_index])
        if find_match_again[target_index] == 'pickChamp':
            time.sleep(15)  # <--- CHECAR ESTO LUEGO

            # Check if match was rejected
            launcher_region = (currentWindow.x, currentWindow.y,
                            currentWindow.width, currentWindow.height)
            accept_button = getButtonLauncher('accept', launcher_region)

            if accept_button == None:
                print("Picking champion...")
                for n in range(5):
                    currentWindow.click(
                        targets['pickChamp']['x'] + n * targets['pickChamp']['x_gap'], targets['pickChamp']['y'])
                    time.sleep(0.4)
                target_index += 1
            else:
                target_index -= 1

        else:
            currentWindow.searchAndClickUntilFound(
                find_match_again[target_index], launcher_width, window_title=launcher_title)
            target_index += 1


def cycle_fromBeginning():
    findMatchFromLauncher()
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
