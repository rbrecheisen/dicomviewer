import os
import shutil
from pathlib import Path
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QLineEdit,
    QCheckBox,
)
from PySide6.QtGui import QDesktopServices
from dicomviewer.widgets.pages.page import Page
from dicomviewer.widgets.pages.dicomsummary.progresscounter import ProgressCounter
from dicomviewer.widgets.pages.dicomsummary.dicomsummarytreeview import DicomSummaryTreeView
from dicomviewer.widgets.pages.dicomsummary.dicomsummaryattributesview import DicomSummaryAttributesView
from dicomviewer.processes.createdicomsummaryprocess import CreateDicomSummaryProcess
from dicomviewer.utils.logmanager import LogManager

LOG = LogManager()


class DicomSummaryPage(Page):
    def __init__(self, settings):
        super(DicomSummaryPage, self).__init__('dicomsummarypage', 'DICOM Summary', settings)
        self._load_dicom_dir_button = None
        self._copy_selected_series_to_output_dir_button = None
        self._view_output_dir_button = None
        self._view_dicom_attributes_button = None
        self._loading_process = None
        self._progress_counter = None
        self._results_table = None
        self._filter_field = None
        self._select_all_or_none_checkbox = None
        self._dicom_attributes_view = None
        self.init()

    # INITIALIZATION

    def init(self):
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_dicom_dir_button())
        button_layout.addWidget(self.copy_selected_series_to_output_dir_button())
        button_layout.addWidget(self.view_output_dir_button())
        button_layout.addWidget(self.view_dicom_attributes_button())
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(button_layout)
        layout.addWidget(self.filter_field())
        layout.addWidget(self.select_all_or_none_checkbox())
        layout.addWidget(self.results_table())
        self.setLayout(layout)

    # GETTERS

    def load_dicom_dir_button(self):
        if not self._load_dicom_dir_button:
            self._load_dicom_dir_button = QPushButton('Load DICOM root directory...')
            self._load_dicom_dir_button.clicked.connect(self.handle_load_dicom_dir_button)
        return self._load_dicom_dir_button
    
    def copy_selected_series_to_output_dir_button(self):
        if not self._copy_selected_series_to_output_dir_button:
            self._copy_selected_series_to_output_dir_button = QPushButton('Copy selected series to output directory...')
            self._copy_selected_series_to_output_dir_button.clicked.connect(self.handle_copy_selected_series_to_output_dir_button)
        return self._copy_selected_series_to_output_dir_button
    
    def view_output_dir_button(self):
        if not self._view_output_dir_button:
            self._view_output_dir_button = QPushButton('View output directory...')
            self._view_output_dir_button.clicked.connect(self.handle_view_output_dir_button)
        return self._view_output_dir_button
    
    def view_dicom_attributes_button(self):
        if not self._view_dicom_attributes_button:
            self._view_dicom_attributes_button = QPushButton('View DICOM attributes...')
            self._view_dicom_attributes_button.clicked.connect(self.handle_view_dicom_attributes_button)
        return self._view_dicom_attributes_button
    
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
            self._filter_field = QLineEdit(placeholderText='Enter keyword to filter the descriptions...')
            self._filter_field.textEdited.connect(self.handle_filter_field)
        return self._filter_field
    
    def select_all_or_none_checkbox(self):
        if not self._select_all_or_none_checkbox:
            self._select_all_or_none_checkbox = QCheckBox('Select all')
            self._select_all_or_none_checkbox.setChecked(True)
            self._select_all_or_none_checkbox.checkStateChanged.connect(self.handle_selection_changed)
        return self._select_all_or_none_checkbox
    
    def dicom_attributes_view(self):
        if not self._dicom_attributes_view:
            self._dicom_attributes_view = DicomSummaryAttributesView(self)
        return self._dicom_attributes_view
    
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

    def handle_copy_selected_series_to_output_dir_button(self):
        data = self.results_table().data()
        if len(data.keys()) == 0:
            QMessageBox.warning(self, 'Warning', 'No series selected')
            return
        message_box = QMessageBox(
            QMessageBox.Question, 'Choose action', 'Do you want to create separate patient folders?')
        yes = message_box.addButton('Yes', QMessageBox.AcceptRole)
        message_box.addButton('No', QMessageBox.DestructiveRole)
        message_box.exec()
        last_directory = self.settings().get('last_directory')
        dir_path = QFileDialog.getExistingDirectory(dir=last_directory)
        if dir_path:
            clicked = message_box.clickedButton()
            self.clear_directory(dir_path)
            for patient_id, item in data.items():
                target_dir_path = dir_path
                if clicked == yes:
                    target_dir_path = os.path.join(dir_path, patient_id)
                    os.makedirs(target_dir_path, exist_ok=True)
                description = item['description']
                for f_path in item['files']:
                    shutil.copy(f_path, target_dir_path)
                LOG.info(f'Copied DICOM series "{description}" to {target_dir_path}')
            self.settings().set('last_directory', dir_path)

    def handle_view_output_dir_button(self):
        last_directory = self.settings().get('last_directory')
        p = Path(last_directory).expanduser().resolve()
        if not p.exists():
            return
        if p.is_file():
            p = p.parent
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(p)))

    def handle_view_dicom_attributes_button(self):
        self.dicom_attributes_view().exec()

    def handle_filter_field(self, search_pattern):
        self.results_table().filter_model_with_search_pattern(search_pattern)

    def handle_progress(self, progress):
        self.progress_counter().set_progress(progress + 1)

    def handle_finished(self, result):
        self.results_table().update_model(result)

    def handle_failed(self, error):
        QMessageBox.warning(self, 'Error', f'Process failed ({error})')

    def handle_selection_changed(self, value):
        self.results_table().select_all(True if value == Qt.CheckState.Checked else False)

    # HELPERS

    def clear_directory(self, dir_path):
        p = Path(dir_path)
        for child in p.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()