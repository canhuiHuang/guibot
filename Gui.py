from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout
import sys


class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(320, 150)
        self.setWindowTitle("Guibot AutoLevel")

        label_launcher_win = QLabel("Launcher detected")

        label_launcher_win2 = QLabel("Launcher detected2")

        self.button_start = QPushButton("Start", self)
        self.button_start.setCheckable(True)
        self.button_start.move(160, 75)
        self.button_start.clicked.connect(self.start)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add Widgets
        layout.addWidget(label_launcher_win)
        layout.addWidget(label_launcher_win2)
        layout.addWidget(self.button_start)

    def start(self, checked):
        print("ayaya", self, checked)
        self.button_start.setDisabled(True)

        # Find League of Legends Launcher
