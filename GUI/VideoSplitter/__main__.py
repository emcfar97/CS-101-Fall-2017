from PyQt6.QtWidgets import QApplication

from GUI.videosplitter import VideoSplitter

Qapp = QApplication([])

app = VideoSplitter()

Qapp.exec()