from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QApplication, QFileDialog, \
    QLineEdit, QDesktopWidget

from MetaPhoto.MetaPhoto import MetaPhoto


class SelectorRowWidget(QWidget):
    def __init__(self, label: str):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.label = QLabel(text=label)
        self.main_layout.addWidget(self.label)

        self.picker_layout = QHBoxLayout()
        self.main_layout.addLayout(self.picker_layout)

        self.select_button = QPushButton(text="Select folder")
        self.picker_layout.addWidget(self.select_button)

        self.selected_folder_text = QLabel(text="Select a folder")
        self.picker_layout.addWidget(self.selected_folder_text)

        self.picker_layout.addStretch()

        # Make connects
        self.select_button.clicked.connect(self.select_folder)

    def select_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self,
                                                       "Select folder")
        if folder_name:
            self.selected_folder_text.setText(folder_name)


class TagWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.label = QLabel("Choose a tag")
        self.main_layout.addWidget(self.label)

        self.tag_text = QLineEdit()
        self.main_layout.addWidget(self.tag_text)


class MoveWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.center()
        self.setWindowTitle("MetaPhoto: Move files!")
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.source_row = SelectorRowWidget(label="Select folder to move from")
        self.main_layout.addWidget(self.source_row)

        self.target_row = SelectorRowWidget(label="Select the target folder")
        self.main_layout.addWidget(self.target_row)

        self.tag_widget = TagWidget()
        self.main_layout.addWidget(self.tag_widget)

        self.execute_button = QPushButton(text="Move")
        self.main_layout.addWidget(self.execute_button)

        # Connects
        self.execute_button.clicked.connect(self.run_move)

    def center(self):
        center_position = QDesktopWidget().availableGeometry().center()
        # Get geometry and move it
        geometry = self.frameGeometry()
        geometry.moveCenter(center_position)
        # Move widget
        self.move(geometry.topLeft())

    def run_move(self):
        meta = MetaPhoto(source_directory=self.source_row.selected_folder_text.text(),
                         target_directory=self.target_row.selected_folder_text.text(),
                         tag=self.tag_widget.tag_text.text())
        meta.copy()


def init_gui():
    app = QApplication()
    move_widget = MoveWidget()
    move_widget.show()

    app.exec_()
