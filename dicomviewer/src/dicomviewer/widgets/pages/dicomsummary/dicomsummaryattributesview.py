from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QTableView,
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
        self.setWindowTitle('DICOM attributes')
        self.resize(800, 600)

    # GETTERS/SETTERS

    def data(self):
        return self._data

    def set_data(self, data):
        self._data = data
        for patient_id, item in self._data.items():
            pass

    def table_view(self):
        if not self._table_view:
            self._table_view = QTableView()
        return self._table_view