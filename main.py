from Gui import *
from LoLBot import *

# Settings
settingsObj = {
    'language': "spanish",
    'image_accuracy': 0.8
}

# Setup
bot = LoLBot()
bot.loadSettings(settingsObj)

bot.init()
