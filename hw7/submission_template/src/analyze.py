import json
import pandas as pd
import argparse

def decode(coding):
    if coding == 'c':
        return 'course-related'
    elif coding == 'f':
        return 'food-related'
    elif coding == 'r':
        return 'residence-related'
    elif coding == 'o':
        return 'other'
    else:
        return None # bad coding

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')

    args = parser.parse_args()

    d = {'course-related':0, 'food-related':0, 'residence-related':0, 'other':0}
    
    df = pd.read_csv(args.input, sep='\t')
    df = df.groupby(['coding']).size().reset_index(name='count')
    df['coding'] = [decode(x) for x in df['coding']]
    records = df.to_dict(orient='records')
    
    for record in records:
        d[record['coding']] = record['count']

    js = json.dumps(d)
    if not args.output:
        print(js)
    else:
        with open(args.output, 'w') as f:
            json.dump(d, f)

if __name__ == '__main__':
    main()
