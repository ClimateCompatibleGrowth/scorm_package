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


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.0.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
