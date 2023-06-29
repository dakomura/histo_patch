**************************************************************
histo_patch : Patch extraction library for Whole Slide Images
**************************************************************

Overview
==============
histo_patch is a python library to extract patches from annotated region in WSI files (Hamamatsu .ndpi or Aperio .svs).
Hamamatsu .ndpa and QuPath .geojson annotation files are supported. 

Installation
=========================
The package can be installed with ``pip``:

.. code:: console

   $ pip install histo-patch

To run histo_patch, simply run below from console:

.. code:: console

   $ histopatch [something]

Usage:

.. code-block::

   Usage: histopatch [OPTIONS] PATH_TO_WSI PATH_TO_SAVE_DIRECTORY

   Options:
   -a, --annotation_type [ndpa|qupath]
                                    file type of annotation (ndpa or qupath
                                    (GeoJSON(Pretty JSON)))
   -s, --annotation_shape [all|line|area]
                                    annotation shape (all, line, area)
   -c, --color TEXT                used colors (white,black,red,green,blue,cyan
                                    ,magenta,yellow) in annotation for ndpa or (
                                    None,Tumor,Stroma,Immune_cells,Necrosis,Othe
                                    r,Region,Ignore,Positive,Negative) for
                                    QuPath
   --line_as_area                  line annotation in ndpa file is treated as
                                    closed area
   --src_size FLOAT                patch size in the original WSI
   -m, --micrometer                specify src_size in micrometer
                                    (default:pixels)
   --patch_size INTEGER            output patch size
   --num_patch INTEGER             number of patches for each annotation shape
   --nparent INTEGER               number of parent directories kept in the
                                    output
   --help                          Show this message and exit.

Usage
========
histopatch [OPTIONS] PATH_TO_WSI PATH_TO_SAVE_DIRECTORY:

Options

-a, --annotation_type [ndpa|qupath] : File type of annotation (ndpa or qupath (GeoJSON (Pretty JSON)))

-s, --annotation_shape [all|line|area] : Annotation shape (all, line, area)

-c, --color TEXT : Colors used in annotation for ndpa (white, black, red, green, blue, cyan, magenta, yellow) or for QuPath (None, Tumor, Stroma, Immune_cells, Necrosis, Other, Region, Ignore, Positive, Negative)

--line_as_area : Line annotation in ndpa file is treated as closed area

--src_size FLOAT : Patch size in the original WSI

-m, --micrometer : Specify src_size in micrometer (default: pixels)

--patch_size INTEGER : Output patch size

--num_patch INTEGER : Number of patches for each annotation shape

--nparent INTEGER : Number of parent directories kept in the output

--help : Show this message and exit.

Prerequisites
==============

Python version 3.6 or newer.

* tifffile >=2022.5.4
* numpy >=1.20.3
* tripy >=1.0.0
* pyclipper >=1.3.0
* opencv-python >= 4.6.0
* zarr >=2.11.3
* magecodecs >=2022.2.22
* click >=8.1.3


Recommended Environment
=======================

* OS
   * Linux
   * Mac
