from __future__ import print_function
from bs4 import BeautifulSoup
import bs4
import os
import argparse

'''
foldermonitor_path_parser.py
Author: Mark Procopio
October 2022

The purpose of this script is to provide ease for creating a number of nested directories required for folder monitor type applications.
This can be used just to gather and write paths to file, to just create the directory hierarchy structure, or both.
This was developed for a particular xml scheme and can be forked to fit, specifically gather_paths().

Arguments:
--mode 
    full:  gathers all required directores from foldermonitor config files, from tag monitorFolder, then creates directory hierarchy structure if non existent
    write-paths: gathers and writes all required directores from foldermonitor config files, from tag monitorFolder, to textfile
    mkdirs: takes a newline separated file as input. and creates the nested directory hierarchy structure for path if non existent.

When using --mode full, if script returns error because of permission denied, you can temporarily set the permissions of the parent dir to 777, i.e.
/srv/isilon/* 
sudo chmod -R 777 /srv/isilon

You will want to set back to whatever permissions were prior following the procedure.

bs4 requires lxml parser (pip install lxml). 

'''

PATH_LIST = []
global ROOT

def write_to_file():
    file = os.path.join(os.getcwd(),"path-output.txt")
    with open(file,"w") as f:
        for path in PATH_LIST:
            f.write("%s\n" % path)

def import_from_file(filepath):
    file = open(filepath, "r")
    for line in file:
        PATH_LIST.append(line.strip())

#path_flag forces writing only of first String which is the foldermonitor path 
def gather_paths(repo_dir):
    #loop through all the foldermonitor files
    for file in next(os.walk(repo_dir))[2]:
        filename = str(file)
        #pull out files with 'foldermonitor' prefix
        if filename.startswith("foldermonitor"):
            print("file located: %s" % filename)
            soup = BeautifulSoup(open(os.path.join(repo_dir,filename),"r"), features='lxml')
            #loop over all monitorFolder keyword names
            for text_body in soup.find_all("keyword", {"name":"monitorFolder"}):
                #write lock 
                path_flag = 1
                for text in text_body:
                    if type(text) is bs4.element.NavigableString and not text == '\n' and path_flag > 0:
                            #we now have first String param which is the path per foldermonitor config scheme
                            text = text.replace('\n','')
                            text = text.replace('\t','')
                            text = text.strip()
                            PATH_LIST.append(str(text).rstrip('/')) #strip the trailing '/' so that os.path.join doesnt get confused as to parent/child
                            #remove write flag
                            path_flag -=1
        else:
            continue

#chdir to the full path; if it does not exist, then we need to chdir to the parent dir and make the child
def mkdirectory(path):
    try:
        #remove prefixed '/' so os.join works
        _path = path[1:]
        os.chdir(_path)
        return 

    except OSError as e:
        if e.errno == 2: #full path directory does not exist
            split_tuple = os.path.split(path)
            parent = split_tuple[0] # .split() returns a 2-tuple of parent, and child
            child = split_tuple[1]
            mkdirectory(parent)
            print("calling mkdir parent: %s" % parent)
            print("child: %s" % child)
            os.mkdir(child)
            join = os.path.join(os.getcwd(), child)
            os.chdir(join)
            return
        if e.errno == 17:
            print("%s already exists" %path)
            return

        else:
            print(e)
            return    

def mkdir_procedure():
    print("--------BEGIN MKDIR PROCEDURE--------")
    for path in PATH_LIST:
        print("~~~ path: %s ~~~" % path)
        #set current working directory
        os.chdir(ROOT)
        path_test = os.path.join(ROOT, path[1:]) #slice path to omit leading '/' otherwise join breaks
        if not os.path.isdir(path_test):
            mkdirectory(path)
        else:
            print("%s exists" % path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--mode', help='modes: {full: gather and make paths, write-paths: write paths to textfile only, mkdirs: make list of dirs specified', 
        choices=['full','write-paths','mkdirs'], required=True)
    parser.add_argument(
        '--pathlist', help='Specify filepath of a newline separated textfile containing target paths to make', default='.')
    parser.add_argument(
        '--dir', help='Directory where foldermonitor config files are located')
    parser.add_argument(
        '--root', help='Base Parent directory for dirs to be created. Set to \"/home/evertz\" if unspecified' , default='/home/evertz')
    args = parser.parse_args()

    ROOT=args.root

    print("=====/////BEGIN SCRIPT/////=====")
    if args.mode == "full":
        config_dir = args.dir
        gather_paths(config_dir)
        mkdir_procedure()
    elif args.mode == "write-paths":
        config_dir = args.dir
        gather_paths(config_dir)
        write_to_file()
    elif args.mode == "mkdirs":
        file = args.pathlist
        import_from_file(file)
        mkdir_procedure()