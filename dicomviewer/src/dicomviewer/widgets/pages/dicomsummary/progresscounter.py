from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Qt


class ProgressCounter(QDialog):
    def __init__(self, parent):
        super(ProgressCounter, self).__init__(parent)
        self._progress_label = None
        self._progress_label_text = 'Nr. DICOM series found'
        self._close_button = None
        self.init()

    def init(self):
        self.setWindowTitle('Progress')
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setModal(False)
        self.resize(200, 60)
        layout = QVBoxLayout(self)
        layout.addWidget(self.progress_label())
        layout.addWidget(self.close_button())

    def progress_label(self):
        if not self._progress_label:
            self._progress_label = QLabel(f'{self._progress_label_text}: 0')
        return self._progress_label
    
    def close_button(self):
        if not self._close_button:
            self._close_button = QPushButton('Close')
            self._close_button.clicked.connect(self.hide)
        return self._close_button
    
    def set_progress(self, progress):
        self.progress_label().setText(f'{self._progress_label_text}: {progress}')