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
        series = {}
        for root, dirs, files in os.walk(self.root_dir()):
            for f in files:
                f_path = os.path.join(root, f)
                if is_dicom(f_path):
                    p = load_dicom(f_path, stop_before_pixels=True)
                    if 'SeriesInstanceUID' in p:
                        if p.SeriesInstanceUID not in series.keys():
                            series[p.SeriesInstanceUID] = []
                        series[p.SeriesInstanceUID].append(f_path)
                    self.progress.emit(count)
                    count += 1
        return series
