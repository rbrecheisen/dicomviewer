from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QTableView,
    QHeaderView,
    QSizePolicy,
)
from PySide6.QtGui import (
    QStandardItem, 
    QStandardItemModel,
)

class DicomSummaryAttributesView(QDialog):
    def __init__(self, parent):
        super(DicomSummaryAttributesView, self).__init__(parent)
        self._data = None
        self._table_view = None
        self.init()

    # INITIALIZATION

    def init(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.table_view(), 1)
        self.setWindowTitle('DICOM attributes')
        self.resize(800, 600)

    # GETTERS/SETTERS

    def data(self):
        return self._data
    
    def set_data(self, data):
        self._data = data

    def update_table_for(self, attribute_name):
        if self.data():
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(['description', attribute_name])
            for suid, series_info in self.data().items():
                model.appendRow([
                    QStandardItem(series_info['description']), 
                    QStandardItem(str(series_info[attribute_name]))
                ])
            self.table_view().setModel(model)
            self.table_view().setSortingEnabled(True)
            self.table_view().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            h = self.table_view().horizontalHeader()
            h.setStretchLastSection(False)
            h.setSectionResizeMode(0, QHeaderView.Stretch)
            h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            h.setMinimumSectionSize(80)

    def table_view(self):
        if not self._table_view:
            self._table_view = QTableView()
        return self._table_view