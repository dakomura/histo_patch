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

   $ pip install histo_patch

To run histo_patch, simply run below from console:

.. code:: console

   $ histo_patch [something]

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

Recommended Environment
=======================

* OS
   * Linux
   * Mac
