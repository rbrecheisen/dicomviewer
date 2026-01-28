import os
from dicomviewer.processes.process import Process
from dicomviewer.utils.utils import is_dicom, load_dicom, is_jpeg2000_compressed


class CreateDicomSummaryProcess(Process):
    def __init__(self, root_dir):
        super(CreateDicomSummaryProcess, self).__init__()
        self._root_dir = root_dir

    # GETTERS

    def root_dir(self):
        return self._root_dir

    def execute(self):
        count = 0
        for root, dirs, files in os.walk(self.root_dir()):
            for f in files:
                f_path = os.path.join(root, f)
                if is_dicom(f_path):
                    self.progress.emit(count)
        return "some result"
