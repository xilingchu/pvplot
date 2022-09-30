# PVPLOT

## Introduction
PVPLOT is a series of python scripts for [Paraview][]. This series of scripts is to ensure the consistency of the same kind of figures while keep it's efficiency and conveience.
These scripts will include the common post-processing figures in CFD, such as streamline, flow field, and pressure distribution.
This repo will also contains a document to introduce the basic usage of PVPLOT.

[Paraview]: http://www.paraview.org

## Usage
You can use these scripts through Paraview client or use pvpython on terminal.
If you want to use it in Paraview client, you should firstly copy the **pvscripts.py**, **utils.py**, and **loadpvcc.py** to the library in the installation directory,
```bash
cp pvscripts.py utils.py loadpvcc.py [path-to-paraview]/lib/[python]/site-packages
```
and then you can import the scripts in Paraview client.

---
If you want to use it in terminal. You can use
```
pvpython [scripts]
```
to use them.

## Document
You can find the usage of Paraview python scripts in [Paraview official document][1], or just see [here][2] to get the specific usage for CFD.

[1]:https://docs.paraview.org/_/downloads/en/v5.10.1/pdf/
[2]:doc/document.md
