import keyboard
import win32api
import win32con
import time
import random


def click(x, y, sleepTime=0.01):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(sleepTime)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def right_click(x, y, sleepTime=0.01):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(sleepTime)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)


def press_key(key_name):
    keyboard.press(key_name)
    time.sleep(random.randint(1, 10) / 100)
    keyboard.release(key_name)
    time.sleep(0.1)


def attackWalk(x, y, sleepTime=0.06):
    keyboard.press('a')
    time.sleep(random.randint(1, 10) / 100)
    keyboard.release('a')
    time.sleep(0.06)
    click(x, y, sleepTime)


def exitNotPressed():
    return not (keyboard.is_pressed('ctrl+escape') or keyboard.is_pressed('ctrl+shift+q'))


def typeInChat(text):
    press_key('enter')
    time.sleep(0.6)
    for char in text:
        press_key(char)
    time.sleep(0.2)
    press_key('enter')
    time.sleep(0.2)
