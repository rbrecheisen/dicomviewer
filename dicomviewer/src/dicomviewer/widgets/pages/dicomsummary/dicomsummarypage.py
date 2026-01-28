from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QMessageBox,
)
from dicomviewer.widgets.pages.page import Page
from dicomviewer.processes.dummyprocess import DummyProcess
from dicomviewer.utils.logmanager import LogManager

LOG = LogManager()


class DicomSummaryPage(Page):
    def __init__(self, settings):
        super(DicomSummaryPage, self).__init__('dicomsummarypage', 'DICOM Summary', settings)
        self._load_dicom_dir_button = None
        self._loading_process = None
        self.init()

    # INITIALIZATION

    def init(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.load_dicom_dir_button())
        self.setLayout(layout)

    # GETTERS

    def load_dicom_dir_button(self):
        if not self._load_dicom_dir_button:
            self._load_dicom_dir_button = QPushButton('Load DICOM root directory')
            self._load_dicom_dir_button.clicked.connect(self.handle_load_dicom_dir_button)
        return self._load_dicom_dir_button
    
    # EVENT HANDLERS

    def handle_load_dicom_dir_button(self):
        last_directory = self.settings().get('last_directory')
        dir_path = QFileDialog.getExistingDirectory(dir=last_directory)
        if dir_path:
            self.settings().set('last_directory', dir_path)
            self._loading_process = DummyProcess()
            self._loading_process.progress.connect(lambda progress: LOG.info(f'progress: {progress}'))
            self._loading_process.finished.connect(self.handle_process_finished)
            self._loading_process.failed.connect(self.handle_process_failed)
            self._loading_process.start()

    def handle_process_finished(self):
        QMessageBox.information(self, 'Info', 'Process finished')

    def handle_process_failed(self):
        QMessageBox.warning(self, 'Error', 'Process failed')