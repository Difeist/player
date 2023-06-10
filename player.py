import time

from PyQt6.QtCore import QUrl, QTimer, Qt
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QProgressBar, \
    QHBoxLayout, QSlider, QSizePolicy, QListWidget
from PyQt6.QtGui import QIcon


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        #настройки окна:
        self.setWindowTitle("MusicPlayer")
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(0, 0, 550, 300)
        self.setMaximumSize(550, 300)
        self.setMinimumSize(550, 300)

        #подключаем медиа плейер
        self.playlist = []
        self.index_track = 0
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.track_name = QLabel('Сейчас проигрывается: ')
        self.main_layout.addWidget(self.track_name)

        self.addButton = QPushButton("Add File", self)
        self.main_layout.addWidget(self.addButton)

        self.addButton.setStyleSheet(
            'QPushButton {background: white; color:black; border:2px solid black; border-radius: 10px; padding:10px;}'
            'QPushButton:hover {background: black; color:white;}')

        #Центральная панель
        self.center_layout = QHBoxLayout()
        self.main_layout.addLayout(self.center_layout)

        self.playButton = QPushButton("Play", self)
        self.center_layout.addWidget(self.playButton)

        self.playButton.setStyleSheet(
            'QPushButton {background: white; color:black; border:2px solid black; border-radius: 10px; padding:10px;}'
            'QPushButton:hover {background: black; color:white;}')

        self.pauseButton = QPushButton("Pause", self)
        self.center_layout.addWidget(self.pauseButton)
        self.pauseButton.setStyleSheet(
            'QPushButton {background: white; color:black; border:2px solid black; border-radius: 10px; padding:10px;}'
            'QPushButton:hover {background: black; color:white;}')

        self.stopButton = QPushButton("Stop", self)
        self.center_layout.addWidget(self.stopButton)
        self.stopButton.setStyleSheet(
            'QPushButton {background: white; color:black; border:2px solid black; border-radius: 10px; padding:10px;}'
            'QPushButton:hover {background: black; color:white;}')

        self.volume_slider = QSlider()
        self.volume_slider.setOrientation(Qt.Orientation.Horizontal)
        self.volume_slider.setValue(50)
        self.volume_slider.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.volume_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.center_layout.addWidget(self.volume_slider)

        self.nextButton = QPushButton("Next", self)
        self.center_layout.addWidget(self.nextButton)
        self.nextButton.setStyleSheet(
            'QPushButton {background: white; color:black; border:2px solid black; border-radius: 10px; padding:10px;}'
            'QPushButton:hover {background: black; color:white;}')


        self.prevButton = QPushButton("Prev", self)
        self.center_layout.addWidget(self.prevButton)

        self.prevButton.setStyleSheet(
            'QPushButton {background: white; color:black; border:2px solid black; border-radius: 10px; padding:10px;}'
            'QPushButton:hover {background: black; color:white;}')

        #временные метки
        self.time_layout = QHBoxLayout()
        self.main_layout.addLayout(self.time_layout)

        self.label_position = QLabel('00:00')
        self.time_layout.addWidget(self.label_position)

        self.label_duration = QLabel('05:50')
        self.label_duration.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.time_layout.addWidget(self.label_duration)

        self.time_line = QSlider(Qt.Orientation.Horizontal)
        self.main_layout.addWidget(self.time_line)

        self.list_track = QListWidget()
        self.main_layout.addWidget(self.list_track)
        #self.list_track.addItem('Hello')

        #события запуска функций
        self.playButton.clicked.connect(self.play)
        self.stopButton.clicked.connect(self.stop)
        self.pauseButton.clicked.connect(self.pause)
        self.time_line.sliderMoved.connect(self.set_position)
        self.volume_slider.sliderMoved.connect(self.set_volume)
        self.addButton.clicked.connect(self.add)
        self.nextButton.clicked.connect(self.next)
        self.prevButton.clicked.connect(self.prev)

    def add(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Music File", ".", "MP3 Files (*.mp3)")
        if not filename:
            return
        track = str(filename).split('/')[-1]
        self.list_track.addItem(track)
        self.playlist.append(filename)

    def play(self):
        if len(self.playlist) > 0:
            time.sleep(.1)
            if self.playlist[self.index_track] == self.player.source().path():
                self.player.play()
                return
            self.player.stop()
            filename = self.playlist[self.index_track]
            self.player.setSource(QUrl.fromLocalFile(filename))
            self.player.positionChanged.connect(self.update_time)
            track = str(filename).split('/')[-1]
            self.track_name.setText(f'Сейчас проигрывается: {track}')
            self.time_line.setRange(0, int(self.player.duration() / 1000))
            self.player.play()

    def stop(self):
        self.player.stop()

    def pause(self):
        self.player.pause()

    def update_time(self):
        position = self.player.position() / 1000
        duration = self.player.duration() / 1000
        minutes, seconds = divmod(position, 60)
        total_minutes, total_seconds = divmod(duration, 60)
        self.label_position.setText(f"{int(minutes)}:{int(seconds)}")
        self.label_duration.setText(f"{int(total_minutes)}:{int(total_seconds)}")
        self.time_line.setValue(int(position))

    def set_position(self, position):
        self.player.setPosition(position * 1000)

    def set_volume(self, position):
        self.audio_output.setVolume(position / 100)

    def next(self):
        if self.index_track < len(self.playlist) - 1:
            self.stop()
            self.index_track += 1
            self.play()

    def prev(self):
        if self.index_track > 0:
            self.stop()
            self.index_track -= 1
            self.play()


if __name__ == "__main__":
    app = QApplication([])
    player = MusicPlayer()
    player.show()
    app.exec()
