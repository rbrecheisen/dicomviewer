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
    
    def update_model(self, series_dict, search_pattern=None):
        self._series_dict = series_dict
        self._model = self.build_model_from_series_dict(self._series_dict, search_pattern)
        self.setModel(self._model)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.Stretch)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(3, 40)

    def filter_model_with_search_pattern(self, search_pattern):
        if self.series_dict():
            self.update_model(self.series_dict(), search_pattern)

    def build_model_from_series_dict(self, series_dict, search_pattern=None):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['description', 'thickness', 'patient_id', 'nr_files'])
        for suid, series_info in series_dict.items():
            description = series_info.get('description', '')
            if search_pattern is None or (search_pattern is not None and self.matches(search_pattern, series_info)):
                patient_id = series_info.get('patient_id', '')
                files = series_info.get('files', [])
                nrfiles = len(files)
                thickness = series_info.get('thickness', 0)
                description_item = QStandardItem(description)
                description_item.setData(suid, role=Qt.UserRole)
                description_item.setFlags(description_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                description_item.setCheckState(Qt.CheckState.Checked if self._all_selected else Qt.CheckState.Unchecked)
                patient_item = QStandardItem(patient_id)
                nrfiles_item = QStandardItem(str(nrfiles))
                thickness_item = QStandardItem(str(thickness))
                model.appendRow([description_item, thickness_item, patient_item, nrfiles_item])
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
                if description_item.checkState() == Qt.CheckState.Checked:
                    suid = description_item.data(role=Qt.UserRole)
                    series_info = self.series_dict()[suid]
                    if suid not in data.keys():
                        data[suid] = series_info
        return data
    
    def matches(self, search_pattern, series_info):
        def contains(item, info):
            for k, v in info.items():
                if item in str(v).lower():
                    return True
            return False
        search_pattern = search_pattern.lower()
        if search_pattern is None or search_pattern == '':
            return True
        if '|' in search_pattern:
            items = search_pattern.split('|')
            for item in items:
                if item != '' and contains(item, series_info):
                    return True
            return False
        if '&' in search_pattern:
            items = search_pattern.split('&')
            for item in items:
                if not contains(item, series_info):
                    return False
            return True
        return contains(search_pattern, series_info)