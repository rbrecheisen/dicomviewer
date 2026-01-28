import dicomviewer.resources.dicomviewer_rc
from PySide6.QtCore import Qt, QByteArray, QTimer
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFileDialog,
)
from PySide6.QtGui import (
    QGuiApplication,
    QAction,
    QIcon,
    QColor,
)
from dicomviewer.settings import Settings
from dicomviewer.widgets.centraldockwidget import CentralDockWidget
from dicomviewer.widgets.logdockwidget import LogDockWidget
from dicomviewer.widgets.pages.page import Page


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._settings = None
        self._central_dockwidget = None
        self._log_dockwidget = None
        self._page = None
        self.init()

    # INITIALIZATION

    def init(self):
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.central_dockwidget())
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.log_dockwidget())
        self.setWindowTitle('DICOM Viewer 1.0')
        self.setWindowIcon(QIcon(self.settings().get('mainwindow/icon_path')))
        self.load_geometry_and_state()
        self.statusBar().showMessage('Ready')

    # GETTERS

    def settings(self):
        if not self._settings:
            self._settings = Settings('nl.rbeesoft', 'dicomviewer')
            self._settings.set('mainwindow/icon_path', ':/icons/dicomviewer')
        return self._settings
    
    def central_dockwidget(self):
        if not self._central_dockwidget:
            self._central_dockwidget = CentralDockWidget(self)
            self._central_dockwidget.add_page(self.page(), self.page().name())
            self._central_dockwidget.select_panel(self.page().name())
        return self._central_dockwidget
    
    def log_dockwidget(self):
        if not self._log_dockwidget:
            self._log_dockwidget = LogDockWidget(self)
        return self._log_dockwidget
    
    def page(self):
        if not self._page:
            self._page = Page(name='page', title='')
        return self._page
    
    # EVENT HANDLERS

    def closeEvent(self, _):
        self.save_geometry_and_state()

    # HELPERS

    def load_geometry_and_state(self):
        geometry = self.settings().get('mainwindow/geometry')
        state = self.settings().get('mainwindow/state')
        if isinstance(geometry, QByteArray) and self.restoreGeometry(geometry):
            if isinstance(state, QByteArray):
                self.restoreState(state)
            return
        self.resize(1024, 1024)
        self.center_window()        

    def save_geometry_and_state(self):
        self.settings().set('mainwindow/geometry', self.saveGeometry())
        self.settings().set('mainwindow/state', self.saveState())

    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.geometry().width()) / 2
        y = (screen.height() - self.geometry().height()) / 2
        self.move(int(x), int(y))
