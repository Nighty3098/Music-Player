import datetime
import fnmatch
import os
import sys
from tkinter import filedialog

import pretty_errors
from pygame import mixer
from PyQt5 import *
from PyQt5 import QtWidgets, uic

window = uic.loadUiType("window.ui")[0]

path = "/home/night/Music"
pattern = "*.mp3"

mixer.init()


class MyClass(QtWidgets.QMainWindow, window):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        global ifFirstStart, isPause
        isFirstStart = True
        isPause = True

        self.PauseButton.clicked.connect(self.pause)
        self.NextButton.clicked.connect(self.next_track)
        self.PrevButton.clicked.connect(self.prev_track)
        self.PlayButton.clicked.connect(self.play)
        self.StartButton.clicked.connect(self.select)
        # self.openFolderButton.clicked.connect(self.select_music_folder(self))

        with open("style.qss", "r") as file:
            style_sheet = file.read()

        self.listTrack.viewport().setStyleSheet(style_sheet)

        for (
            root,
            dirs,
            files,
        ) in os.walk(path):
            for filename in fnmatch.filter(files, pattern):
                self.listTrack.addItem(filename)

    def select(self):
        self.title.setText(self.listTrack.currentItem().text())
        print(self.listTrack.currentItem().text())
        mixer.music.load(path + "/" + self.listTrack.currentItem().text())
        print(path + "/" + self.listTrack.currentItem().text())
        mixer.music.play()

    def pause(self):
        mixer.music.pause()
        # self.PauseButton.setText("Play")

    def play(self):
        # if isPause == True:
        mixer.music.unpause()
        # isPause = False
        # self.PauseButton.setText("Pause")

        global current_position
        current_position = int(mixer.music.get_pos())
        self.progressBar.setValue(current_position)

    def next_track(self):
        # next_track = self.listTrack.count()
        next_track = self.listTrack.currentRow()
        print(next_track)
        next_track = next_track + 1

        item = self.listTrack.item(next_track)
        next_track_title = item.text()

        self.listTrack.setCurrentItem(item)

        print(next_track)
        print(next_track_title)

        self.title.setText(next_track_title)

        mixer.music.load(path + "/" + next_track_title)
        mixer.music.play()

    def prev_track(self):
        # next_track = self.listTrack.count()
        prev_track = self.listTrack.currentRow()
        print(prev_track)
        prev_track = prev_track - 1

        item = self.listTrack.item(prev_track)
        prev_track_title = item.text()

        self.listTrack.setCurrentItem(item)

        print(prev_track)
        print(prev_track_title)

        self.title.setText(prev_track_title)

        mixer.music.load(path + "/" + prev_track_title)
        mixer.music.play()


"""
    def select_music_folder(self):
        global path
        path = filedialog.askdirectory()
        for (
            root,
            dirs,
            files,
        ) in os.walk(path):
            for filename in fnmatch.filter(files, pattern):
                self.listTrack.addItem(filename)
"""

app = QtWidgets.QApplication(sys.argv)
myWin = MyClass()
myWin.show()
app.exec_()
