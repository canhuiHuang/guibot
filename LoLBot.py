import datetime as dt

from anyio import current_time
from Bot import *
import json
from PIL import Image
from Gui import *

launcher_width = 1280
launcher_height = 720
game_width = 1920
game_height = 1080


class LoLBot(Bot):
    # Targets & Regions
    # Raw numbers are fractional numbers related to either the width or height of the LoL Launcher
    # Check guide.jpg & guide.clip for reference.
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

        self.gui = createGui('LightGrey2')
        self.logs = ''
        self._launcher_status = ''
        self._game_status = ''
        self.initialized = False

    # Initialize Bot with GUI
    def init(self):
        while True:
            event, values = self.gui.read(timeout=20)

            if event == sg.WIN_CLOSED:
                break

            if (self._launcher_status == 'green' or self._game_status == 'green') and not self.initialized:
                self._activateStartBtn()

            if event == '-BTN_START-':
                self.initialized = True
                self._deactivateStartBtn()
                while exitNotPressed():
                    self.findMatch()
                    self.waitGameToLaunch()
                    self.playGame()
                    self.postGame()
                self.consoleLog('Bot was stopped.')
                self.initialized = False

            if event == 'Save logs(.txt)':
                file_name = f"LOG{dt.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.txt"
                file = open(file_name, 'w')
                file.write(self.logs)
                file.close()

            self.getActiveWindows()

        self.gui.close()

    # GUI Stuff
    def consoleLog(self, text):
        self.logs += f'{text}\n'
        print(text)
        self.gui['-CONSOLE-'].update(self.logs)
        self.gui.refresh()

    def _activateStartBtn(self):
        self.gui['-BTN_START-'].update(
            button_color='#b7f27c', disabled=False)

    def _deactivateStartBtn(self):
        self.gui['-BTN_START-'].update(
            button_color='#d4d4d4', disabled=True)

    def loadSettings(self, settingsObj):
        translation_file = open("translation.json")
        translated = json.load(translation_file)
        targets_file = open("targets.json")
        targets = json.load(targets_file)

        pyautogui.FAILSAFE = False
        self.image_accuracy = settingsObj['image_accuracy']
        self.language = settingsObj['language']
        self.launcher_title = translated[self.language]['launcher_title']
        self.game_title = translated[self.language]['game_title']
        self.loadFocusRegions(targets)

    def focusWindow(self, window_title):
        # Focus window
        windowObj = getWindowObj(window_title)
        while windowObj == None:
            time.sleep(0.05)
            self.consoleLog('looking for window', getWindowObj(window_title))
            windowObj = getWindowObj(window_title)
        windowObj.activate()

        # Update current window position ( In case the window is moving )
        self.setWindow(windowObj)

    def _setLauncherLight(self, color):
        self.gui['-LIGHT_LAUNCHER-'].update(
            source=f'resources/gui/{color}Circle16x16.png')

    def _setGameLight(self, color):
        self.gui['-LIGHT_GAME-'].update(
            source=f'resources/gui/{color}Circle16x16.png')

    def getActiveWindows(self):
        self.getLauncherWindow()
        self.getGameWindow()

    def getLauncherWindow(self):
        self.launcher_window = getWindowObj(self.launcher_title)

        color = ''
        if self.launcher_window != None:
            if self.launcher_window.width == launcher_width and self.launcher_window.height == launcher_height:
                color = 'green'
            else:
                color = 'orange'

            self.gui['-RES_LAUNCHER-'].update(
                f'{self.launcher_window.width}x{self.launcher_window.height}')
        else:
            color = 'red'
            self.gui['-RES_LAUNCHER-'].update('')

        if self._launcher_status != color:
            self._launcher_status = color
            self._setLauncherLight(color)

    def getGameWindow(self):
        self.game_window = getWindowObj(self.game_title)

        color = ''
        if self.game_window != None:
            if self.game_window.width == game_width and self.game_window.height == game_height:
                color = 'green'
            else:
                color = 'orange'

            self.gui['-RES_GAME-'].update(
                f'{self.game_window.width}x{self.game_window.height}')
        else:
            color = 'red'

            self.gui['-RES_GAME-'].update('')

        if self._game_status != color:
            self._game_status = color
            self._setGameLight(color)

    def getTarget(self, target, language_independent=False, type="launcher", region=None, confidence=0.8):
        image_confidence = self.image_accuracy
        if confidence != 0.8:
            image_confidence = confidence
        window_width = self.launcher_window.width
        if type == 'launcher':
            self.focusWindow(self.launcher_title)
        elif type == 'game':
            window_width = self.game_window.width
            self.focusWindow(self.game_title)

        image_path = f"resources/{self.language}/{target}{window_width}.png"
        if language_independent:
            image_path = f"resources/{target}{window_width}.png"

        # Target found box
        focus_region = self.getFocusRegionFromStore(target, type)
        if region != None:
            focus_region = region
        return pyautogui.locateOnScreen(
            image_path, region=focus_region, confidence=image_confidence)

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
        w = self.launcher_proportions["width"]
        h = self.launcher_proportions["height"]
        if type == 'game':
            w = self.game_proportions["width"]
            h = self.game_proportions["height"]

        region_x = int(
            (self.stored_regions[target_name]['x'] / w) * self.width)
        region_y = int(
            (self.stored_regions[target_name]['y'] / h) * self.height)
        search_width = int(
            (self.stored_regions[target_name]['search_width'] / w) * self.width)
        search_height = int(
            (self.stored_regions[target_name]['search_height'] / h) * self.height)

        return (self.x + region_x, self.y + region_y, search_width, search_height)

    def click(self, dx, dy, type):
        w_fr = self.launcher_proportions["width"]
        h_fr = self.launcher_proportions["height"]
        x = self.launcher_window.left
        y = self.launcher_window.top
        w = self.launcher_window.width
        h = self.launcher_window.height
        if type == 'game':
            w_fr = self.game_proportions["width"]
            h_fr = self.game_proportions["height"]
            x = self.game_window.left
            y = self.game_window.top
            w = self.game_window.width
            h = self.game_window.height

        click(x + int((dx / w_fr) * w),
              (y + int((dy/h_fr) * h)))

    def searchAndClickUntilFound(self, target_name, type, click_func, wait=0.0, language_independent=False, limit=-1):
        time.sleep(wait)

        clicked = False
        stop = False
        count = 0
        while not clicked and not stop:
            self.consoleLog(f'Searching... {target_name}')
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
            image_path, region=self.getFocusRegionsFromStore(target_name, type), confidence=self.image_accuracy)

        if on_view_location != None:
            self.consoleLog(f"Target {target_name} found")
            with Image.open(image_path) as img:
                # Click on the center of the target
                click_func(int(on_view_location[0] + img.size[0] / 2),
                           int(on_view_location[1] + img.size[1] / 2))

            return True
        else:
            self.consoleLog(f"{target_name} not found...")

        time.sleep(0.4)
        return False

    def getDimensionFromFractions(self, x_fr, y_fr, proportions, float=False, type='launcher'):
        x = self.launcher_window.left + \
            (x_fr / proportions['width']) * self.launcher_window.width
        y = self.launcher_window.top + \
            (y_fr / proportions['height']) * self.launcher_window.height
        if type == 'game':
            x = self.game_window.left + \
                (x_fr / proportions['width']) * self.game_window.width
            y = self.game_window.top + \
                (y_fr / proportions['height']) * self.game_window.height

        if float:
            return (x, y)
        return (int(x), int(y))

    def getProportionFromTitle(self, window_title):
        if window_title == self.launcher_title:
            return self.launcher_proportions
        elif window_title == self.game_title:
            return self.game_proportions

    def getCoordsByTarget(self, target_name, type):
        cur_x = self.launcher_window.left
        cur_y = self.launcher_window.top
        cur_width = self.launcher_window.width
        cur_height = self.launcher_window.height
        width_proportion = self.launcher_proportions['width']
        height_proportion = self.launcher_proportions['height']
        if type == 'game':
            cur_x = self.game_window.left
            cur_y = self.game_window.top
            cur_width = self.game_window.width
            cur_height = self.game_window.height
            width_proportion = self.game_proportions['width']
            height_proportion = self.game_proportions['height']

        return (int(cur_x + (self.stored_regions[target_name]['x'] /
                width_proportion) * cur_width), int(cur_y + (self.stored_regions[target_name]['y'] /
                                                             height_proportion) * cur_height))

    def moveCursorTo(self, x_fr, y_fr, type, sleepTime=0.15):

        window_title = self.launcher_title
        if type == 'launcher':
            self.focusWindow(self.launcher_title)
        else:
            self.focusWindow(self.game_title)
            window_title = self.game_title

        win32api.SetCursorPos(self.getDimensionFromFractions(
            x_fr, y_fr, self.getProportionFromTitle(window_title), type=type))
        time.sleep(sleepTime)

    def attackWalkRandomCoord(self):
        x = self.game_window.left + \
            random.randint(0, self.game_window.width - 1)
        y = self.game_window.top + \
            random.randint(0, self.game_window.height - 1)

        attackWalk(x, y)

    def findMatch(self):
        find_match = ['play', 'ai', 'intermedia', 'confirm', 'playAgain',
                      'findMatch', 'accept', 'pickChamp', 'lockChamp']
        game_has_started = False

        try:
            while exitNotPressed() and not game_has_started:
                self.consoleLog('Finding match...')

                time.sleep(0.6)

                # Click on buttons
                for target_name in find_match:

                    # Enters champioon select
                    if target_name == 'pickChamp':
                        time.sleep(4)
                        self.consoleLog("Picking champion...")
                        for n in range(5):
                            self.click(
                                self.stored_regions['pickChamp']['x'] + n * self.stored_regions['pickChamp']['x_gap'], self.stored_regions['pickChamp']['y'], 'launcher')
                            time.sleep(0.2)
                    else:
                        self.consoleLog(
                            f"Looking for target: {target_name}...")
                        target = self.getTarget(target_name)
                        if target != None:
                            self.consoleLog(f"Target {target_name} found")
                            with Image.open(f"resources/{self.language}/{target_name}{self.launcher_window.width}.png") as img:

                                # Click on the center of the target
                                click(int(target[0] + img.size[0] / 2),
                                      int(target[1] + img.size[1] / 2))
                        else:
                            self.consoleLog(f"{target_name} not found.")

                        time.sleep(0.6)

                windows = pyautogui.getWindowsWithTitle(self.game_title)
                if len(windows) > 0:
                    self.consoleLog('Game about to start...')
                    game_has_started = True
        except Exception as e:
            self.consoleLog(f'WARN: {e}')

    def waitGameToLaunch(self):
        game_running = False
        cur_time = 0
        timeout = 6
        while exitNotPressed() and not game_running:
            time.sleep(5)
            self.consoleLog('Waiting for game to start...')
            windows = pyautogui.getWindowsWithTitle(self.game_title)
            if len(windows) > 0:
                self.consoleLog('Game has started.')
                self.setWindow(windows[0])
                self.getGameWindow()
                time.sleep(20)
                game_running = True
            if cur_time >= timeout:
                break
            cur_time += 1
            print(cur_time)

    def playGame(self):
        def buy(item_name):
            press_key('p')

            time.sleep(2)
            if self.getTarget('searchShopItem', type='game') != None:
                self.searchAndClickUntilFound(
                    'searchShopItem', 'game', click, limit=4)
                time.sleep(0.5)
                typewrite(self.stored_regions[item_name]['search_term'])
                time.sleep(1.5)
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

        try:
            while exitNotPressed() and self.getTarget('continue', type='game') == None and game_in_progress:

                if len(pyautogui.getWindowsWithTitle(self.game_title)) > 0:
                    # Check health
                    low_health_point = self.getCoordsByTarget(
                        'lowHp', type='game')
                    if pyautogui.pixelMatchesColor(low_health_point[0], low_health_point[1], expectedRGBColor=(1, 13, 7), tolerance=12):
                        self.consoleLog(
                            'player is low health! Walking to fountain...')

                        # Walk to fountain
                        fountain = self.getCoordsByTarget(
                            'fountain', type='game')
                        right_click(fountain[0], fountain[1])
                        time.sleep(10)

                        # Buy something from shop
                        if buy_count < len(items_to_buy):
                            self.consoleLog(
                                f'Trying to purchase {items_to_buy[buy_count]}...')
                            if buy(items_to_buy[buy_count]):
                                buy_count += 1

                        # Set new lane to go
                        lane_to_go = random.randint(1, 3)

                    # Attack forward (Top, Mid, Bot)
                    if aggresive_pushing:
                        nexus = self.getCoordsByTarget('nexus', type='game')
                        attackWalk(nexus[0], nexus[1])
                    elif lane_to_go == 1:
                        topA = self.getCoordsByTarget('topA', type='game')
                        attackWalk(topA[0], topA[1])
                    elif lane_to_go == 2:
                        midA = self.getCoordsByTarget('midA', type='game')
                        attackWalk(midA[0], midA[1])
                    elif lane_to_go == 3:
                        botA = self.getCoordsByTarget('botA', type='game')
                        attackWalk(botA[0], botA[1])

                    # Miscellaneous Periodic checks
                    if seconds % 6 == 0:
                        # Update current window position ( In case the window is moving )
                        self.focusWindow(self.game_title)

                        # Lock camera
                        unlock_icon = self.getTarget(
                            'unlockedCamera', language_independent=True, type='game', confidence=0.98)
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

                            click(self.game_window.left + int((x_fr / w) * self.game_window.width),
                                  (self.game_window.top + int((y_fr / h) * self.game_window.height)))
                            time.sleep(random.random())

                        # Skills up
                        if self.getTarget('skillUp', language_independent=True, type='game'):
                            self.searchAndClick(
                                'skillUp', 'game', True, click)

                    # Every 1:30 minute, trigger between defensive and aggresive pushing
                    if seconds % 90 == 0 and seconds != 0:
                        aggresive_pushing = not aggresive_pushing

                        fountain = self.getCoordsByTarget(
                            'fountain', type='game')
                        right_click(fountain[0], fountain[1])
                        # Wait for hp to get full
                        time.sleep(10)

                        # Buy something from shop
                        buy('krakenSlayer')

                    # 5% chance to move back a little
                    if random.randint(1, 20) == 1:
                        fountain = self.getCoordsByTarget(
                            'fountain', type='game')
                        right_click(fountain[0], fountain[1])

                    time.sleep(1)

                    def aggresivePushing():
                        if aggresive_pushing:
                            return ' aggresively.'
                        else:
                            return '.'
                    self.consoleLog(
                        f"Time: {seconds}s. Pushing lane: {['top', 'mid', 'bot'][lane_to_go - 1]}{aggresivePushing()}")
                    seconds += 1

                else:
                    time.sleep(32)
                    if len(pyautogui.getWindowsWithTitle(self.game_title)) <= 0:
                        game_in_progress = False

            # Game is over
            continue_button = self.getTarget('continue', type='game')
            if continue_button != None:
                with Image.open(f"resources/{self.language}/continue{self.game_window.width}.png") as img:
                    # Click on the center of the target
                    click(int(continue_button[0] + img.size[0] / 2),
                          int(continue_button[1] + img.size[1] / 2))
                    # Press Enter in case click fails
                    press_key('enter')
        except Exception as e:
            self.consoleLog(f'Something happened: {e}')

    def postGame(self):
        try:
            # Focus launcher
            self.getLauncherWindow()
            self.focusWindow(self.launcher_title)

            time.sleep(10)
            # honor opponents
            click(int(self.launcher_window.width / 2),
                  (int(self.launcher_window.height / 2)))

            # accept gifts & level ups
            launcher_region = (self.launcher_window.left, self.launcher_window.top,
                               self.launcher_window.width, self.launcher_window.height)

            play_again_button = self.getTarget('playAgain')
            while exitNotPressed() and play_again_button == None:
                time.sleep(4)

                # Look if a free champion is given
                for champ in self.stored_regions['championsPosition']:
                    champ_box = self.getTarget(
                        champ['name'], language_independent=True, region=launcher_region)

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
        except Exception as e:
            self.consoleLog(f'WARN: {e}')
