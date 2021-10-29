import json
import argparse
from datetime import datetime
import pytz
import sys

def convertToUTC(s:str) -> str:
    dt = datetime.strptime(s,'%Y-%m-%dT%H:%M:%S%z')
    return str(dt.astimezone(pytz.utc))

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    return parser.parse_args(args)

def load_json(s):
    try:
        obj = json.loads(s)
        return obj
    except:
        return

def process_title(json_obj):
    """
    Return True if the obj is to be kept, process the obj if necessary;
    Return False if the obj is invalid
    """
    if 'title_text' in json_obj:
        json_obj['title'] = json_obj.pop('title_text')
        return True
    return 'title' in json_obj

def process_time(json_obj):
    """
    Try to convert the 'createdAt' field from ISO to UTC time, discard invalid time formate.
    If the field is not present, keep the object and do nothing.

    Return True if the object is to be kept and False otherwise.
    """
    if 'createdAt' in json_obj:
        try:
            json_obj['createdAt'] = convertToUTC(json_obj['createdAt'])
            return True
        except:
            return False
    return True

def process_author(json_obj):
    """
    Return True if the object contains the field 'author' that is not empty nor N/A
    """
    return ('author' in json_obj) and json_obj['author'] and (json_obj['author'] != 'N/A')

def process_total_count(json_obj):
    """
    Try to cast the total_count field to int.
    Discard objects that fails the casting.
    Keep objects without the field.

    Return True if the object is to be kept and False otherwise.
    """
    if 'total_count' in json_obj:
        try:
            json_obj['total_count'] = int(json_obj['total_count'])
            return True
        except:
            return False
    return True

def process_tags(json_obj):
    """
    Process the tags filed so that it is a list containing only individual words. Assume the tags field is always of type list.
    Keep the object regardless.
    """
    if 'tags' in json_obj:
        json_obj['tags'] = [tag for s in json_obj['tags'] for tag in s.split()]
    return True


def main(arguments = sys.argv[1:]):
    args = parse_args(arguments)

    data = []
    with open(args.input, 'r') as f:
        for line in f:
            # load each line and skip bad strings
            obj = load_json(line)
            if obj is None:
                continue
        
            # filter object
            if process_title(obj) and process_time(obj) and process_author(obj) and process_total_count(obj) and process_tags(obj):
                data.append(obj)

    # write to output
    with open(args.output, 'w') as f:
        for line in data:
            f.write(json.dumps(line) + '\n')            

if __name__ =='__main__':
    main()
