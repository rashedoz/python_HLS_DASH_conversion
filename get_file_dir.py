import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QInputDialog, QLineEdit, QFileDialog,QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon

import sys
import ffmpeg_streaming
from ffmpeg_streaming import Representation
import os, sys
from pathlib import Path
from tqdm import tqdm

# HLS representation
# rep_360 = Representation(width=640, height=360, kilo_bitrate=276)
# rep_480 = Representation(width=854, height=480, kilo_bitrate=750)
# rep_720 = Representation(width=1280, height=720, kilo_bitrate=2048)


# DASH representation
rep_144 = Representation(width=256, height=144, kilo_bitrate=95)
rep_240 = Representation(width=426, height=240, kilo_bitrate=150)
rep_360 = Representation(width=640, height=360, kilo_bitrate=276)
rep_480 = Representation(width=854, height=480, kilo_bitrate=750)
rep_720 = Representation(width=1280, height=720, kilo_bitrate=2048)
rep_1080 = Representation(width=1920, height=1080, kilo_bitrate=4096)
rep_1440 = Representation(width=2560, height=1440, kilo_bitrate=6096)

def progress(percentage, ffmpeg):
        # You can update a field in your database
        # You can also create a socket connection and show a progress bar to users
        sys.stdout.write("\rTranscoding...(%s%%)[%s%s]" % (percentage, '#' * percentage, '-' * (100 - percentage)))
        sys.stdout.flush()

##### Dialog widget
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'HLS & DASH Conversion'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        button = QPushButton('Select Folder', self)
        button.setToolTip('Choose folder to convert files')
        button.move(100,70)
        button.clicked.connect(self.on_click)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)
        
        self.show()
    

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        ###### Get folder path
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(file)

        # Open a file
        path = file ##"/Volumes/bacbon_workplace/BacBon_Videos/python_tr_test"
        dirs = os.listdir( path )

        # This would print all the files and directories
        for file in tqdm(dirs):
            if file.endswith(".mp4"):
                print (file)
                folder_name = Path(file).stem
                video_path = path+"/"+file
                new_dir_location = path+"/"+folder_name
                trancoded_file_name = new_dir_location + "/" + folder_name + ".m3u8"
                # trancoded_file_name = new_dir_location + "/" + folder_name + ".mpd"
                
                if os.path.isdir(video_path):
                    print("skipping folder ")

                #Check if folder already exists
                elif os.path.exists(new_dir_location):
                    print("Folder already exists")
                else:
                    print("Creating new folder")
                    os.makedirs(new_dir_location)

                print(video_path)
                print(trancoded_file_name)

                
                # Trancode videos to DASH Format
                # (
                #     ffmpeg_streaming
                #         .dash(video_path, adaption='"id=0,streams=v id=1,streams=a"')
                #         .format('libx265')
                #         .add_rep(rep_360, rep_480, rep_720,)
                #         # .add_rep(rep_144, rep_240)
                #         .package(trancoded_file_name,progress=progress)
                # )

                # Trancode videos to HLS Format
                (
                ffmpeg_streaming
                    .hls(video_path, hls_time=3)
                    .format('libx264')
                    .add_rep(rep_144,rep_240,rep_360,rep_480, rep_720)
                    # .add_rep(rep_360)
                    .package(trancoded_file_name,progress=progress)
                    
                )

                # self.completed = 0
                # while self.completed < 10000:
                #     self.completed += 0.0001
                #     self.progress.setValue(self.completed)



   







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

