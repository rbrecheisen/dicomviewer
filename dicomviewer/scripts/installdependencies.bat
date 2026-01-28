@echo off

@rem Make sure activate the "dicomviewer" environment before running
@rem the command below!
call mamba install -c conda-forge ^
    pyside6 ^
    numpy ^
    pandas ^
    pydicom ^
    pillow ^
    poetry ^
    matplotlib ^
    SimpleITK