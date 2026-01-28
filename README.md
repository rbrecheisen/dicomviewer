# DICOM Viewer
Tool for summary visualization and management of DICOM data


## Core features
- List DICOM series in root folder
- Filter by DICOM attribute
- View summary stats
- Copy selected series to output folder


## Design considerations
After the summarization process I have a dictionary of series. I could list them in 
PySide6 table view, perhaps with unfolding to show the individual DICOM images. And
selection checkboxes in front of each series. 

If I want to have a filter field above the table, what do I filter on? Series Description
initially? Because that's what I'm showing in the table for each series anyway. It makes
most sense to filter on Series Description. What other series-level attributes do we have?

    - Series description
    - Pixel spacing
    - Tube voltage
    - Rows/columns
    - Patient ID/name
    - Manufaturer

There are a lot of attributes I could show. Perhaps I need a widget that allows me to add/
remove attributes to show in the table.