from PySide6.QtWidgets import QTreeView, QHeaderView
from PySide6.QtGui import (
    QStandardItem, 
    QStandardItemModel,
)
from PySide6.QtCore import Qt


class DicomSummaryTreeView(QTreeView):
    def __init__(self, parent):
        super(DicomSummaryTreeView, self).__init__(parent)
        self._series_dict = None
        self.init()

    def init(self):
        self.setRootIsDecorated(True)
        self.setItemsExpandable(True)
        self.setSortingEnabled(True)
        self.expandToDepth(0)

    def series_dict(self):
        return self._series_dict
    
    def update_model(self, series_dict, keyword=None):
        self._series_dict = series_dict
        self.setModel(self.build_model_from_series_dict(self._series_dict, keyword))
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(1, QHeaderView.Stretch)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.setColumnWidth(0, 80)
        self.setColumnWidth(2, 40)

    def filter_model_with_keyword(self, keyword):
        if self.series_dict():
            self.update_model(self.series_dict(), keyword)

    def build_model_from_series_dict(self, series_dict, keyword=None):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['patient_id', 'description', 'nr_files'])
        for suid, series_info in series_dict.items():
            description = series_info.get('description', '')
            if keyword is None or (keyword is not None and keyword in description):
                patient_id = series_info.get('patient_id', '')
                files = series_info.get('files', [])
                nrfiles = len(files)
                patient_id_item = QStandardItem(patient_id)
                description_item = QStandardItem(description)
                description_item.setData(suid, role=Qt.UserRole)
                nrfiles_item = QStandardItem(str(nrfiles))
                model.appendRow([patient_id_item, description_item, nrfiles_item])
                for f in files:
                    f_item = QStandardItem(f)
                    description_item.appendRow([f_item, QStandardItem(''), QStandardItem('')])
        return model