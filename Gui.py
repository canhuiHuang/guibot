import PySimpleGUI as sg


def createGui(theme):
    sg.theme(theme)
    log_menu = ['menu', ['Save logs(.txt)']]
    layout = [
        [sg.Text('Launcher:', font='Roboto, 15', size=(8, 1)), sg.Input('', key='-RES_LAUNCHER-', disabled=True, text_color='#333333', size=(10, 1)),
         sg.Image('resources/gui/whiteCircle16x16.png', key='-LIGHT_LAUNCHER-')],
        [sg.Text('Game:', font='Roboto, 15', size=(8, 1)), sg.Input('', key='-RES_GAME-', disabled=True,
                                                                    text_color='#333333', size=(10, 1)), sg.Image('resources/gui/whiteCircle16x16.png', key='-LIGHT_GAME-')],
        [sg.Image('resources/gui/greenCircle16x16.png', pad=((10, 0), 15)), sg.Text(': Detected', font='Default, 10'), sg.Image('resources/gui/orangeCircle16x16.png', pad=((10, 0), 15)),
         sg.Text(': Something is wrong'), sg.Image('resources/gui/redCircle16x16.png', pad=((10, 0), 15)), sg.Text(': Not detected')],
        [sg.Text('Make sure you have the default game settings.', font='Roboto, 11')],
        [sg.Text('To stop the bot:\nHold Ctrl + Shift + Q or Ctrl + Escape until the bot stops',
                 text_color='#de8245')],
        [sg.Button('Start', key='-BTN_START-',
                   expand_x=True, size=(30, 2), pad=(0, 20), font='Roboto, 15', disabled=True)],
        [sg.Multiline(background_color='#333333', text_color='#e3c059', pad=(1, 0), size=(
            30, 10), expand_x=True, key='-CONSOLE-', justification='left', disabled=True, autoscroll=True, right_click_menu=log_menu)]
    ]

    return sg.Window('Guibot AutoLevel', layout, icon='resources/icon.ico')
