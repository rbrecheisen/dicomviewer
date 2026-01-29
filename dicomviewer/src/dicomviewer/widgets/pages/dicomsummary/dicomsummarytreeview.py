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
        self._model = None
        self._all_selected = True
        self.init()

    def init(self):
        self.setRootIsDecorated(True)
        self.setItemsExpandable(True)
        self.setSortingEnabled(True)
        self.expandToDepth(0)
        self.setUniformRowHeights(True)

    def series_dict(self):
        return self._series_dict
    
    def update_model(self, series_dict, keyword=None):
        self._series_dict = series_dict
        self._model = self.build_model_from_series_dict(self._series_dict, keyword)
        self.setModel(self._model)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 40)

    def filter_model_with_keyword(self, keyword):
        if self.series_dict():
            self.update_model(self.series_dict(), keyword)

    def build_model_from_series_dict(self, series_dict, keyword=None):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['description', 'patient_id', 'nr_files'])
        for suid, series_info in series_dict.items():
            description = series_info.get('description', '')
            if keyword is None or (keyword is not None and keyword in description):
                patient_id = series_info.get('patient_id', '')
                files = series_info.get('files', [])
                nrfiles = len(files)
                description_item = QStandardItem(description)
                description_item.setData(suid, role=Qt.UserRole)
                description_item.setFlags(description_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                description_item.setCheckState(Qt.CheckState.Checked if self._all_selected else Qt.CheckState.Unchecked)
                patient_item = QStandardItem(patient_id)
                nrfiles_item = QStandardItem(str(nrfiles))
                model.appendRow([description_item, patient_item, nrfiles_item])
                for f in files:
                    f_item = QStandardItem(f)
                    description_item.appendRow([f_item, QStandardItem(''), QStandardItem('')])
        return model
    
    def select_all(self, mode=True):
        if self._model:
            root = self._model.invisibleRootItem()
            for idx in range(root.rowCount()):
                description_item = root.child(idx, 0)
                if mode:
                    description_item.setCheckState(Qt.CheckState.Checked)
                else:
                    description_item.setCheckState(Qt.CheckState.Unchecked)
            self._all_selected = mode

    def data(self):
        data = {}
        if self._model:
            root = self._model.invisibleRootItem()
            for idx in range(root.rowCount()):
                description_item = root.child(idx, 0)
                patient_item = root.child(idx, 1)
                if patient_item.text() not in data.keys():
                    data[patient_item.text()] = {
                        'description': description_item.text(),
                        'files': [],
                    }
                for idx2 in range(description_item.rowCount()):
                    file_item = description_item.child(idx2)
                    data[patient_item.text()]['files'].append(file_item.text())
        return data