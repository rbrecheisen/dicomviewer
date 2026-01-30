from rbeesoft.app.ui.rbeesoftmainwindow import RbeesoftMainWindow
from dicomviewer.widgets.pages.dicomsummary.dicomsummarypage import DicomSummaryPage


class MainWindow(RbeesoftMainWindow):
    def __init__(self, app_icon):
        super(MainWindow, self).__init__(
            bundle_identifier='rbeesoft.nl',
            app_name='dicomviewer',
            app_title='DICOM Summary Viewer 1.0',
            width=800,
            height=600,
            app_icon=app_icon,
        )
        self.add_page(DicomSummaryPage(self.settings()), home_page=True)