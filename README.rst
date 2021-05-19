=============
scorm_package
=============


Convert a folder of HTML files into a SCORM package.


Description
===========

Course_1.zip is a valid scorm package.
File ``imsmanifest.xml`` is the definition of what goes in the package.
The other XSD files are required boilerplate that we don't need to fiddle with.
Folder `Course_1/res/` is where we put slides, HTML files and any other files that are needed
(in this example a PDF file), but could be an image file embedded within the HTML.

In ``imsmanifest.xml`` there is a resource tag that defines what files are in the package and which one
should be the start when the learning management system (LMS) launches the package.

```xml
<resource identifier="resource" type="webcontent" adlcp:scormtype="sco" href="res/test.html">
<file href="res/test.html"/>
<file href="res/GitCoreConcepts.pdf"/>
</resource>
```

Wrapping the contents of the folder up as a zip (as it is in the folder here)
is what produces a scorm package.

Steps to script things up
-------------------------

1. Set up a template scorm folder
   this contains all the boilerplate XSDs and templates etc

2. copy boilerplate into a tmp folder

3.  Use Jinja2 template for imsmanifest
    We can use a Jinja2 template to make the resource file list and starting resource into variables
    e.g. something like::

        <resource identifier="resource" type="webcontent" adlcp:scormtype="sco" href="{{resource}}">
        {% for resource in resourcelist %}
                    <file {{ resource }} >
        {% endfor %}
        </resource>

- create imsmanifest from list of files the user provides and put that in tmp folder
- copy user's input files into `/res/` in the tmp folder
- zip up the tmp folder to produce a scorm package.


Notes on running the scorm.py script which produces a SCORM package
-------------------------------------------------------------------

Notes on producing slides for SCORM package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Create markdown file with slide source (test.md in this example).

    Folder structure

    /source/test.md
    /source/images/<image files to include>

    Use pandoc to compile self-contained HTML slides with the slidy framework (requires connection to web to get slidy CSS).

    https://pandoc.org/MANUAL.html#producing-slide-shows-with-pandoc

    ## Create HTML slides:
    pandoc -t slidy --self-contained test.md -o test.html

    (can also create PDF slides - requires pdfLaTeX)
    pandoc -t beamer test.md -V theme:Warsaw -o test.pdf

#Running the Python script
~~~~~~~~~~~~~~~~~~~~~~~~~~

    You just need to provide two arguments with the python script:
    The first argument is the name you want to give your scorm package.
    The second argument is the name of your created self-contained html file (created in the Prerequisites)

#For help run -h or --help "python scorm.py -h" otherwise contact thomas.hutcheson@moneysupermarket.com


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.0.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
