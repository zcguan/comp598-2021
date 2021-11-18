import argparse
import sys
import pandas as pd
import os
import json

def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-d', '--dialog')
    args = parser.parse_args(args)

    stop_words = []
    with open(os.path.join(os.path.dirname(__file__), '..', 'data',  'stopwords.txt')) as f:
        for line in f:
            if not line.startswith('#'):
                stop_words.append(line.strip('\n'))
    
    pony_names = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']
    punctuations = ['(', ')', '[', ']', ',', '-', '.', '?', '!', ':', ';', '#', '&']

    df = pd.read_csv(args.dialog, usecols=['pony','dialog'])

    # lowercase
    df['pony'] = df['pony'].str.lower()
    df['dialog'] = df['dialog'].str.lower()

    # keep only ponies
    df = df[df['pony'].isin(pony_names)]
    
    # strip punctuations
    for punc in punctuations:
        df['dialog'] = df['dialog'].str.replace(punc, ' ', regex=False)
    
    # groupby pony
    df = df.groupby('pony').agg(' '.join).reset_index()
    
    # word breakdown
    df['dialog'] = df['dialog'].str.split()
    
    # transform to dict and remove stop words and non alphabetical 
    d = {}
    for pony in pony_names:
        if pony in df['pony'].values:
            d[pony] = [w for w in df[df['pony'] == pony].iloc[0]['dialog'] if w.isalpha() and w not in stop_words]
    
    result = {}
    total_count = {}
    for pony in d:
        count = {}

        # word count for each pony
        for w in d[pony]:
            if w in count:
                count[w] += 1
            else:
                count[w] = 1
        
        # calculate total word count for all dialog
        for w in count:
            if w in total_count:
                total_count[w] += count[w]
            else:
                total_count[w] = count[w]
        
        result[pony] = count

    # remove < 5 total occurances
    r = {}
    for pony in result:
        freq = {}
        for w in result[pony]:
            if total_count[w] >= 5:
                freq[w] = result[pony][w]
        r[pony] = freq
    
    # check output directory
    if os.path.dirname(args.output):
        os.makedirs(os.path.dirname(args.output), exist_ok=True)

    with open(args.output, 'w') as f:
        json.dump(r, f)

if __name__ == '__main__':
    main()
