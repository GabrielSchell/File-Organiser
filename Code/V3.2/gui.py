import sys, time, json, os.path
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QProgressBar, QLabel
from PyQt5.QtCore import QTimer, QStandardPaths, Qt

from lib import intialiser, organiser, estimation

class FolderSelectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Folder Selector')
        self.setGeometry(100, 100, 400, 200)

        # Create buttons
        self.update_button = QPushButton('ORGANISE FOLDER', self)

        # Create a progress bar and a label for "FINISHED!"
        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()  # Hide the progress bar initially
        self.progress_label = QLabel(self)
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.hide()  # Hide the label initially

        # Connect button signals to slots
        self.update_button.clicked.connect(self.update_folder)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.update_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_label)
        self.setLayout(layout)

        # Flag to track if the operation is finished
        self.operation_finished = False

        # Create a QTimer for showing "FINISHED!" after 1 second
        self.finished_timer = QTimer(self)
        self.finished_timer.timeout.connect(self.show_finished_label)


    def update_folder(self):
        folder_path = self.select_folder()
        if folder_path:
            print("Selected folder for UPDATE ORGANISED FOLDER:", folder_path)
            max=2*int(estimation(folder_path))
            self.progress_bar.setValue(0)
            self.progress_label.hide()
            self.progress_bar.show()         
            count=intialiser(folder_path, self.progress_bar, max=max)
            organiser(folder_path, self.progress_bar, count=count, max=max)
            print("MAX: ",max)
            self.finished_timer.start(1000)

    def select_folder(self):
        self.progress_label.hide()
        options = QFileDialog.Options()
        default_path = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
        folder_dialog = QFileDialog.getExistingDirectory(self, "Select Folder", default_path, options=options)
        return folder_dialog.replace("\\", "/")

    def show_finished_label(self):
        # Update the label to show "FINISHED!" when the QTimer triggers
        self.progress_bar.hide()
        self.progress_label.setText("FINISHED!")
        self.progress_label.show()
        self.operation_finished = True
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FolderSelectorApp()
    window.show()
    sys.exit(app.exec_())
