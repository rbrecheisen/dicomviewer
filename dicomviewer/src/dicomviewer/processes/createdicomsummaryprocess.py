import os
import pandas as pd
from rbeesoft.app.ui.processes.process import Process
from dicomviewer.utils.utils import is_dicom, load_dicom


class CreateDicomSummaryProcess(Process):
    def __init__(self, root_dirs):
        super(CreateDicomSummaryProcess, self).__init__()
        self._root_dirs = root_dirs

    # EXECUTION

    def execute(self):
        count = 0
        series_dict = {}
        for root_dir in self._root_dirs:
            for root, dirs, files in os.walk(root_dir):
                for f in files:
                    f_path = os.path.join(root, f)
                    if is_dicom(f_path):
                        p = load_dicom(f_path, stop_before_pixels=True)
                        if 'SeriesInstanceUID' in p:
                            if p.SeriesInstanceUID not in series_dict.keys():
                                series_dict[p.SeriesInstanceUID] = {
                                    'patient_id': p.PatientID if 'PatientID' in p else '',
                                    'description': p.SeriesDescription if 'SeriesDescription' in p else '',
                                    'rows': p.Rows if 'Rows' in p else 0,
                                    'cols': p.Columns if 'Columns' in p else 0,
                                    'spacingx': p.PixelSpacing[0] if 'PixelSpacing' in p else 0.0,
                                    'spacingy': p.PixelSpacing[1] if 'PixelSpacing' in p else 0.0,
                                    'thickness': p.SliceThickness if 'SliceThickness' in p else 0.0,
                                    'image_type': p.ImageType if 'ImageType' in p else '',
                                    'manufacturer': p.Manufacturer if 'Manufacturer' in p else '',
                                    'files': [],
                                }
                                self.progress.emit(count)
                                count += 1
                            series_dict[p.SeriesInstanceUID]['files'].append(f_path)
                            print(f'Adding {f_path}')
                        else:
                            print(f'DICOM file has no SeriesInstanceUID')
        return series_dict
    
    # HELPERS

    def build_df_from_series_dict(self, series_dict):
        data = {
            'patient_id': [],
            'description': [],
            'rows': [],
            'cols': [],
            'spacingx': [],
            'spacingy': [],
            'thickness': [],
            'image_type': [],
            'manufacturer': [],
            'nr_files': [],
        }
        for k, v in series_dict.items():
            data['description'].append(v['description'])
            data['rows'].append(v['rows'])
            data['cols'].append(v['cols'])
            data['spacingx'].append(v['spacingx'])
            data['spacingy'].append(v['spacingy'])
            data['thickness'].append(v['thickness'])
            data['manufacturer'].append(v['manufacturer'])
            data['nr_files'].append(len(v['files']))
        df = pd.DataFrame(data=data)
        return df