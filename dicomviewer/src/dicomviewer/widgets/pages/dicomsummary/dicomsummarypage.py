import json
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QMessageBox,
    QLineEdit,
)
from dicomviewer.widgets.pages.page import Page
from dicomviewer.widgets.pages.dicomsummary.progresscounter import ProgressCounter
from dicomviewer.widgets.pages.dicomsummary.dicomsummarytreeview import DicomSummaryTreeView
from dicomviewer.processes.createdicomsummaryprocess import CreateDicomSummaryProcess
from dicomviewer.utils.logmanager import LogManager

LOG = LogManager()


class DicomSummaryPage(Page):
    def __init__(self, settings):
        super(DicomSummaryPage, self).__init__('dicomsummarypage', 'DICOM Summary', settings)
        self._load_dicom_dir_button = None
        self._loading_process = None
        self._progress_counter = None
        self._results_table = None
        self._filter_field = None
        self.init()

    # INITIALIZATION

    def init(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.load_dicom_dir_button())
        layout.addWidget(self.filter_field())
        layout.addWidget(self.results_table())
        self.setLayout(layout)

    # GETTERS

    def load_dicom_dir_button(self):
        if not self._load_dicom_dir_button:
            self._load_dicom_dir_button = QPushButton('Load DICOM root directory')
            self._load_dicom_dir_button.clicked.connect(self.handle_load_dicom_dir_button)
        return self._load_dicom_dir_button
    
    def progress_counter(self):
        if not self._progress_counter:
            self._progress_counter = ProgressCounter(self)
        return self._progress_counter
    
    def results_table(self):
        if not self._results_table:
            self._results_table = DicomSummaryTreeView(self)
        return self._results_table
    
    def filter_field(self):
        if not self._filter_field:
            self._filter_field = QLineEdit(placeholderText='Enter keyword')
            self._filter_field.textEdited.connect(self.handle_filter_field)
        return self._filter_field
    
    # EVENT HANDLERS

    def handle_load_dicom_dir_button(self):
        last_directory = self.settings().get('last_directory')
        dir_path = QFileDialog.getExistingDirectory(dir=last_directory)
        if dir_path:
            self.progress_counter().show()
            self.settings().set('last_directory', dir_path)
            self._loading_process = CreateDicomSummaryProcess(dir_path)
            self._loading_process.progress.connect(self.handle_progress)
            self._loading_process.finished.connect(self.handle_finished)
            self._loading_process.failed.connect(self.handle_failed)
            self._loading_process.start()

    def handle_filter_field(self, value):
        self.results_table().filter_model_with_keyword(value)

    def handle_progress(self, progress):
        self.progress_counter().set_progress(progress + 1)

    def handle_finished(self, result):
        self.results_table().update_model(result)

    def handle_failed(self, error):
        QMessageBox.warning(self, 'Error', f'Process failed ({error})')