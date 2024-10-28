#!/bin/python

'''
@author procopim
@details 
  Find an arbitray key/value tag pair in a json payload that is arbitrarily nested

  For example:
    { "field": [{
                "name": "shapeTag",
                 "id": [],
                "value": [{
                    "value": "__mp4"}]
              }]
    }

  cmd: python find_tag.py shapeTag value source_json.json
    >> [{"value": "__mp4"}]

'''


import json
import argparse

def search_object_keys(object_dict, tag, valuename):
    
    try:
        res = None
        for k,v in object_dict.items():
            try:
                if v == tag:
                    print(f"\nMatched tag: {tag}\n")
                    return object_dict[valuename]
                elif isinstance(v, list):
                    for obj in v:
                        res = search_object_keys(obj, tag, valuename)
                        if res:
                            return res
                elif isinstance(v, dict):
                    res = search_object_keys(v, tag, valuename)
                    if res:
                        return res
            except KeyError as e:
                print(f"No such tag value name for {tag}: {e}")
                continue
            except Exception as e:
                print(f"\nError in items loop: {e}\n")
            continue
        return res
    except AttributeError as e:
        print(f"Error: {e}")
        return None
    

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("tag_key", help="tag to search for")
    argparser.add_argument("tag_value_name", help="name of the value tag to return")
    argparser.add_argument("file", help="file containing json payload")
    args = argparser.parse_args()

    file = args.file
    tag = args.tag_key
    valuename = args.tag_value_name

    try:
        with open(file, 'r') as f:
            data = json.load(f) # dict object
    except:
        print(f"Could not open file {file}")
        exit(1)
    
    print(search_object_keys(data, tag, valuename))
    

