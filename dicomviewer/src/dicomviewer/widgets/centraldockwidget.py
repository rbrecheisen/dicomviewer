from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QDockWidget,
    QStackedWidget,
)
from dicomviewer.settings import Settings
from dicomviewer.utils.logmanager import LogManager

LOG = LogManager()


class CentralDockWidget(QDockWidget):
    def __init__(self, parent):
        super(CentralDockWidget, self).__init__(parent)
        self._settings = None
        self._title_label = None
        self._stacked_widget = None
        self._pages = None
        self.init()

    # INITIALIZATION

    def init(self):
        layout = QVBoxLayout()
        layout.addWidget(self.title_label())
        layout.addWidget(self.stacked_widget())
        container = QWidget()
        container.setLayout(layout)
        self.setObjectName('centraldockwidget') # Needed for saving geometry/state
        self.setWidget(container)

    # GETTERS/SETTERS

    def settings(self):
        if not self._settings:
            self._settings = Settings()
        return self._settings
    
    def title_label(self):
        if not self._title_label:
            self._title_label = QLabel('')
            self._title_label.setStyleSheet('color: black; font-weight: bold; font-size: 14pt;')
        return self._title_label
    
    def stacked_widget(self):
        if not self._stacked_widget:
            self._stacked_widget = QStackedWidget()
        return self._stacked_widget
    
    def pages(self):
        if not self._pages:
            self._pages = {}
        return self._pages
    
    # HELPERS

    def add_page(self, page, name):
        self.pages()[name] = page
        self.stacked_widget().addWidget(page)

    def select_panel(self, name):
        page = self.pages().get(name, None)
        if page:
            self.title_label().setText(page.title())
            self.stacked_widget().setCurrentWidget(page)