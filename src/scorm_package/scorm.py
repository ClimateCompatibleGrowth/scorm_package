#!/usr/bin/python
import os
import sys
from distutils.dir_util import copy_tree
from jinja2 import Environment, FileSystemLoader, Template
import zipfile
import shutil
import argparse
import logging
from typing import List

logger = logging.getLogger()


def argumentParser():
    """
    Creates a -h / --help flag that describes what the user is required to do, sets a requirement for two arguments to run the script, 1) scorm package name and 2) the name of a html file.
    """
    parser = argparse.ArgumentParser(add_help=True,
                                     description="Creates a SCORM package from a folder of HTML files")

    parser.add_argument('package_name', action="store",
                        help='Scorm package name')
    parser.add_argument('html_file_name', action="store",
                        help='Path to the folder containing HTML files to package')

    return parser.parse_args()


def create_directories(dirName):
    """
    Create directories
    """
    # Create directory

    try:
        # Create target Directory
        os.mkdir(dirName)
        logger("Directory " , dirName ,  " Created ")
    except FileExistsError:
        logger("Directory " , dirName ,  " already exists")
        exit(1)
    subDirName = dirName+'/res'

    # Create target directory & all intermediate directories if don't exists
    try:
        os.makedirs(subDirName)
        logger("Directory " , subDirName ,  " Created ")
    except FileExistsError:
        logger("Directory " , subDirName ,  " already exists")
    return subDirName


def copy_files(dirName, static):
    """
    Copy xsd files from static folder to named directory
    """

    fromDirectory = static
    toDirectory = dirName
    try:
        copy_tree(fromDirectory, toDirectory)
        logger("Content Copied From " , fromDirectory ,"to", toDirectory,  " Successfully ")
    except FileExistsError:
        logger("Content Failed to Copy From " , fromDirectory ,"to", toDirectory,  "")
        exit(1)


def copy_resources(subDirName, resfiles):
    """
    Copy resource files from ``resfiles`` folder to named directory ``subDirName``
    """

    fromDirectory = resfiles
    toDirectory = subDirName
    try:
        copy_tree(fromDirectory, toDirectory)
        logger("Content Copied From " , fromDirectory ,"to", toDirectory,  " Successfully ")
    except FileExistsError:
        logger("Content Failed to Copy From " , fromDirectory ,"to", toDirectory,  "")
        exit(1)

def resourcelist(resource_content) -> List[str]:
    """
    Gets all the file paths for the content of the newly created sub-directory "/res"
     which is used in jinja_template which edits the imsmanifest.xml file.
    """
    all_resources = os.listdir(resource_content)
    output = [os.path.join("res", f) for f in all_resources ]
    return output

def jinja_template(dirName, all_resources, templatefile):
    """Edits the imsmanifest.xml file, adds a list of the resource files to the xml.

    Arguments
    ---------
    dirName
    all_resources
    templatefile

    """
    # TODO: Move this file operation outside of the function
    with open(templatefile) as f:
        mytext = f.read()

    template = Template(mytext)
    output = template.render(resourcelist=all_resources, title=dirName)

    # TODO: Move this file operation outside of the function
    filepath = os.path.join(dirName, "imsmanifest.xml")
    with open(filepath, 'w') as outfile:
      outfile.write(output)

#----------------------------
#Zip folder to create scorm package
#------------------------------

def retrieve_file_paths(dirName):
    """
    Retrieves the filepath for the directoy being zipped.
    """
    # setup file paths variable
    filePaths = []

    # Read all directory, subdirectories and file lists
    for root, directories, files in os.walk(dirName):
      for filename in files:
          # Create the full filepath by using os module.
          filePath = os.path.join(root, filename)
          filePaths.append(filePath)

    # return all paths
    return filePaths


def zip_directory(dirName):
    """
    The zip_directory function zips the content of the created score_package folder.
    """

  # Assign the name of the directory to zip
    dir_name = dirName

    # Call the function to retrieve all files and folders of the assigned directory

    filePaths = retrieve_file_paths(dir_name)

    # loggering the list of all files to be zipped
    logger('The following list of files will be zipped:')
    for fileName in filePaths:
      logger(fileName)

    # writing files to a zipfile
    zip_file = zipfile.ZipFile(dir_name+'.zip', 'w')
    with zip_file:
      # writing each file one by one
      for file in filePaths:
        zip_file.write(file)

      logger(dir_name+'.zip file is created successfully!')


def delete_directory(dirName):
    """
    The delete_directory function deletes the created folder structure leaving the user with just the zipped scorm package.
    """

    # delete directory
    dirName = dirName

    try:
        # Delete target Directory
        shutil.rmtree(dirName, ignore_errors=False, onerror=None)
        logger("Directory " , dirName ,  " Deleted ")
    except FileExistsError:
        logger("Directory " , dirName ,  " Failed to Delete")


def main():

    args = argumentParser()
    dirName=args.package_name
    htmlresource=args.html_file_name

    subDirName = create_directories(dirName)

    resource_content = os.path.join(dirName, 'res')

    copy_files(dirName=dirName, static='static/')

    copy_resources(subDirName=subDirName, resfiles=htmlresource)

    resources = resourcelist(resource_content)

    jinja_template(dirName = dirName,
                   all_resources =resources,
                   templatefile = "static/imsmanifest.xml")

    zip_directory(dirName = dirName)

    delete_directory(dirName = dirName)

# Call the main function
if __name__ == "__main__":
    main()