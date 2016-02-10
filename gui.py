#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PySide.QtGui import QWidget, QBoxLayout, QFileDialog, QPushButton, QLabel, QFrame
import os
from correlate import correlate


class MainWindow(QWidget, object):
    # noinspection PyUnresolvedReferences
    def __init__(self):
        super(MainWindow, self).__init__()
        self.clip_filename = None
        self.audio_filename = None
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        clip_row = QBoxLayout(QBoxLayout.LeftToRight)
        self.clip_button = QPushButton()
        self.clip_button.clicked.connect(self.open_clip)
        self.clip_button.setText(self.tr("Open clip"))
        clip_row.addWidget(self.clip_button)
        self.clip_view = QLabel()
        clip_row.addWidget(self.clip_view)
        clip_frame = QFrame()
        clip_frame.setLayout(clip_row)
        layout.addWidget(clip_frame)
        audio_row = QBoxLayout(QBoxLayout.LeftToRight)
        self.audio_button = QPushButton()
        self.audio_button.clicked.connect(self.open_audio)
        self.audio_button.setText(self.tr("Open audio"))
        audio_row.addWidget(self.audio_button)
        self.audio_view = QLabel()
        audio_row.addWidget(self.audio_view)
        audio_frame = QFrame()
        audio_frame.setLayout(audio_row)
        layout.addWidget(audio_frame)
        save_row = QBoxLayout(QBoxLayout.LeftToRight)
        self.save_button = QPushButton()
        self.save_button.clicked.connect(self.save)
        self.save_button.setText(self.tr("Save synced clip"))
        save_row.addWidget(self.save_button)
        save_frame = QFrame()
        save_frame.setLayout(save_row)
        layout.addWidget(save_frame)
        self.update_save_button()
        layout.addStretch()
        self.setLayout(layout)
        self.show()

    def open_clip(self):
        self.clip_filename = QFileDialog.getOpenFileName(
            self,
            self.tr("Open Clip"),
            os.getcwd(),
            self.tr("Video Files [.mp4, .ogv, .mkv, .avi, .mov] (*.mp4 *.ogv *.mkv *.avi *.mov);;" +
                    "Audio Files [.flac, .ogg, .wav, .mp3] (*.flac *.ogg *.wav *.mp3)"))[0]
        self.clip_view.setText(self.clip_filename)
        self.update_save_button()

    def open_audio(self):
        self.audio_filename = QFileDialog.getOpenFileName(
            self,
            self.tr("Open Audio"),
            os.getcwd(),
            self.tr("Audio Files [.flac, .ogg, .wav, .mp3] (*.flac *.ogg *.wav *.mp3)"))[0]
        self.audio_view.setText(self.audio_filename)
        self.update_save_button()

    def update_save_button(self):
        self.save_button.setEnabled(bool(self.clip_filename and self.audio_filename))

    def save(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDefaultSuffix("avi")
        dialog.setDirectory(os.getcwd())
        dialog.setNameFilter(self.tr("Video Files [.avi] (*.avi)"))
        if dialog.exec_():
            output_file_name = dialog.selectedFiles()[0]
            correlate(self.clip_filename, self.audio_filename, output_file_name)
