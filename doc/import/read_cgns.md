# Import Data from CGNS file

## Read Data from CGNS File.

You can use CGNSSeriesReader to read the CGNS file.
```python
datafield = CGNSSeriesReader(registrationName=<register name>:str, FileNames=[<filename>:str,...])
```
- **registrationName** is the name show in the Paraview client.
- **FileNames** is a list contains the files you want to import.

## Set the Base
```python
datafield.Bases = [<Basename>:str]
```
- The list will shown in the Paraview client.

## Set the Data You Want to Read
```python
datafield.CellArrayStatus = [<arrayname>:str]
datafield.PointArrayStatus = [<arrayname>:str]
```
- **CellArrayStatus** and **PointArrayStatus** depends on the type in your file. And they are lists contains the array you want to read.
