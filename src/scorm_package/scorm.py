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

import pkg_resources


logger = logging.getLogger()

logging.basicConfig(level=logging.DEBUG)

def create_directories(directory_name):
    """
    Create directories
    """
    # Create directory

    try:
        # Create target Directory
        os.mkdir(directory_name)
        logger.info("Directory %s Created", directory_name)
    except FileExistsError:
        logger.info("Directory %s already exists", directory_name)
        exit(1)
    subdirectory_name = os.path.join(directory_name, 'res')

    # Create target directory & all intermediate directories if don't exists
    try:
        os.makedirs(subdirectory_name)
        logger.info("Directory %s Created", subdirectory_name)
    except FileExistsError:
        logger.info("Directory %s already exists", subdirectory_name)
    return subdirectory_name


def copy_files(dirName, static):
    """
    Copy xsd files from static folder to named directory
    """
    fromDirectory = pkg_resources.resource_filename(__name__, static)
    toDirectory = dirName
    do_a_copy(fromDirectory, toDirectory)


def copy_resources(subDirName, resfiles):
    """
    Copy resource files from ``resfiles`` folder to named directory ``subDirName``
    """
    fromDirectory = resfiles
    toDirectory = subDirName
    do_a_copy(fromDirectory, toDirectory)

def do_a_copy(from_dir, to_dir):
    try:
        copy_tree(from_dir, to_dir)
        logger.info("Content Copied From %s to %s Successfully", from_dir, to_dir)
    except FileExistsError:
        logger.info("Content Failed to Copy From %s to %s", from_dir, to_dir)
        exit(1)

def resourcelist(resource_content) -> List[str]:
    """
    Gets all the file paths for the content of the newly created sub-directory "/res"
     which is used in jinja_template which edits the imsmanifest.xml file.
    """
    all_resources = os.listdir(resource_content)
    output = [os.path.join("res", f) for f in all_resources if f.endswith(".html")]
    return sorted(output)

def jinja_template(dirName: str, all_resources: List, templatefile: str, block: int):
    """Edits the imsmanifest.xml file, adds a list of the resource files to the xml.

    Arguments
    ---------
    dirName : str
        The destination folder for the SCORM package
    all_resources : list
        A list of html file names in the res folder of the package. These
        are assumed to be ordered e.g. from 1 to 4
    templatefile : str
        The text of the Jinja2 template
    block : int
        The number of the lecture block

    """
    # TODO: Move this file operation outside of the function
    with open(templatefile) as f:
        mytext = f.read()

    output = render_template(mytext, all_resources, block)

    # TODO: Move this file operation outside of the function
    filepath = os.path.join(dirName, "imsmanifest.xml")
    with open(filepath, 'w') as outfile:
      outfile.write(output)

def render_template(mytext: str, all_resources: List, block: int) -> str:
    """

    Arguments
    ---------
    mytext : str
        The text of the Jinja2 template
    all_resources : list
        A list of html file names in the res folder of the package. These
        are assumed to be ordered e.g. from 1 to 4
    block : int
        The number of the lecture block

    """
    template = Template(mytext)
    output = template.render(resourcelist=all_resources, block=block)
    return output

#----------------------------
#Zip folder to create scorm package
#------------------------------

def retrieve_file_paths(dirName):
    """
    Retrieves the filepath for the directory being zipped.
    """
    # setup file paths variable
    filePaths = []

    # Read all directory, subdirectories and file lists
    for root, _, files in os.walk(dirName):
      for filename in files:
          # Create the full filepath by using os module.
          filePath = os.path.join(root, filename)
          filePaths.append(filePath)

    # return all paths
    return filePaths


def zip_directory(dir_name):
    """
    The zip_directory function zips the content of the created scorm_package folder.

    Arguments
    ---------
    dir_name: str
        The name of the dirctory to zip
    """

    # Retrieve all files and folders of the assigned directory
    filePaths = retrieve_file_paths(dir_name)

    # logging the list of all files to be zipped
    logger.info('The following list of files will be zipped:')
    for fileName in filePaths:
        logger.info(fileName)

    # writing files to a zipfile
    with zipfile.ZipFile(os.path.join(dir_name, dir_name + '.zip'), 'w') as zip_file:
      # writing each file one by one
      for file_name in filePaths:
        arc_name = os.path.relpath(file_name, dir_name)
        zip_file.write(file_name, arc_name)

      logger.info(f"{dir_name}.zip file was created successfully!")


def delete_directory(dirName):
    """
    The delete_directory function deletes the created folder structure leaving the user with just the zipped scorm package.
    """

    # delete directory
    dirName = dirName

    try:
        # Delete target Directory
        shutil.rmtree(dirName, ignore_errors=False, onerror=None)
        logger.info("Directory %s Deleted ", dirName)
    except FileExistsError:
        logger.info("Directory %s Failed to Delete", dirName)


def main():

    args = argumentParser()
    directory_name = args.directory_name
    html_resource = args.html_resource

    subdirectory_name = create_directories(directory_name)

    copy_files(directory_name, 'static')
    copy_resources(subdirectory_name, html_resource)

    resource_content = os.path.join(directory_name, 'res')
    resources = resourcelist(resource_content)

    templatefile = pkg_resources.resource_filename(__name__, "static/imsmanifest.xml")
    jinja_template(directory_name,
                   resources,
                   templatefile,
                   args.lecture_block_number)

    zip_directory(directory_name)

    delete_directory(directory_name)


def argumentParser():
    """
    Creates a -h / --help flag that describes what the user is required to do, sets a requirement for two arguments to run the script, 1) scorm package name and 2) the name of a html file.
    """
    parser = argparse.ArgumentParser(add_help=True,
                                     description="Creates a SCORM package from a folder of HTML files")

    parser.add_argument('directory_name', action="store",
                        help="Scorm package name e.g. `lecture_block_01`")
    parser.add_argument('html_resource', action="store",
                        help='Path to the folder containing HTML files to package e.g. `lecture_01`')
    parser.add_argument('lecture_block_number', action="store", type=int,
                        help="The number of the lecture block")

    return parser.parse_args()


# Call the main function
if __name__ == "__main__":
    main()