from PySide6.QtWidgets import QWidget


class Page(QWidget):
    def __init__(self, name, title, settings):
        super(Page, self).__init__()
        self._name = name
        self._title = title
        self._settings = settings

    def name(self):
        return self._name

    def title(self):
        return self._title
    
    def settings(self):
        return self._settings