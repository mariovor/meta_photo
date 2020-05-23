from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QApplication


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


class MoveWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MetaPhoto: Move files!")
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        source_row = SelectorRowWidget(label="Select folder to move from")
        self.main_layout.addWidget(source_row)

        target_row = SelectorRowWidget(label="Select the target folder")
        self.main_layout.addWidget(target_row)


def init_gui():
    app = QApplication()
    move_widget = MoveWidget()
    move_widget.show()

    app.exec_()
