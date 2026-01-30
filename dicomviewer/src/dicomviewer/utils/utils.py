import time
import math
import pydicom
import warnings
from pydicom.uid import ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian
from rbeesoft.common.logmanager import LogManager
warnings.filterwarnings("ignore", message="Invalid value for VR UI:", category=UserWarning)

LOG = LogManager()


def current_time_in_milliseconds():
    return int(round(time.time() * 1000))


def current_time_in_seconds() -> int:
    return int(round(current_time_in_milliseconds() / 1000.0))


def elapsed_time_in_milliseconds(start_time_in_milliseconds):
    return current_time_in_milliseconds() - start_time_in_milliseconds


def elapsed_time_in_seconds(start_time_in_seconds):
    return current_time_in_seconds() - start_time_in_seconds


def duration(seconds):
    h = int(math.floor(seconds/3600.0))
    remainder = seconds - h * 3600
    m = int(math.floor(remainder/60.0))
    remainder = remainder - m * 60
    s = int(math.floor(remainder))
    return '{} hours, {} minutes, {} seconds'.format(h, m, s)


def is_dicom(f):
    try:
        pydicom.dcmread(f, stop_before_pixels=True)
        return True
    except pydicom.errors.InvalidDicomError:
        pass
    return False
    

def load_dicom(f, stop_before_pixels=False):
    try:
        return pydicom.dcmread(f, stop_before_pixels=stop_before_pixels)
    except pydicom.errors.InvalidDicomError:
        try:
            p = pydicom.dcmread(f, stop_before_pixels=stop_before_pixels, force=True)
            if hasattr(p, 'SOPClassUID'):
                if not hasattr(p.file_meta, 'TransferSyntaxUID'):
                    LOG.warning(f'DICOM file {f} does not have FileMetaData/TransferSyntaxUID, trying to fix...')
                    p.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
                return p
        except pydicom.errors.InvalidDicomError:
            pass
    return None


def is_jpeg2000_compressed(p):
    if hasattr(p.file_meta, 'TransferSyntaxUID'):
        return p.file_meta.TransferSyntaxUID not in [ExplicitVRLittleEndian, ImplicitVRLittleEndian, ExplicitVRBigEndian]
    return False
