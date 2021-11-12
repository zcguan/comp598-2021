import os
import argparse
import random
import json
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('json_file')
    parser.add_argument('num_posts', type=int)

    args = parser.parse_args()
    
    with open(args.json_file) as f:
        lines = f.readlines()

    max = args.num_posts if args.num_posts <= len(lines) else len(lines)

    posts = random.sample(lines, max)
    
    d = {'name': [], 'title': []}
    for post in posts:
        p = json.loads(post)
        d['name'].append(p['data']['name'])
        d['title'].append(p['data']['title'])

    df = pd.DataFrame.from_dict(d)
    df['coding'] = ''
    
    if os.path.dirname(args.output):
        os.makedirs(os.path.dirname(args.output), exist_ok=True)

    df.to_csv(args.output, sep='\t', index=False)

if __name__ == '__main__':
    main()
