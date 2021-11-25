import json
import argparse
import pandas as pd

def filter_name(pony):
    p = pony.split()
    flag = 'others' in p or 'ponies' in p or 'and' in p or 'all' in p
    return None if flag else pony

def compute_most_frequent(df, col, n):
    d = df[col].value_counts().to_dict()
    l = [(k,v) for k,v in d.items()]
    l.sort(key=lambda x: x[1], reverse=True)
    return [k for k,_ in l[:n]]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    df = pd.read_csv(args.input, usecols=['title','pony'])

    df['pony'] = df['pony'].str.lower()

    # filter speakers
    df['pony'] = [filter_name(p) for p in df['pony']]

    top101 = compute_most_frequent(df, 'pony', 101)
    
    # replace less freq speakers
    df['pony'] = [p if p in top101 else None for p in df['pony']]

    iterator = df.itertuples(index=False)
    
    # prepare result dict
    result = {p:{} for p in top101}

    prev_ep, prev_pony = next(iterator)
    for row in iterator:
        cur_ep, cur_pony = row

        # same episode and different speakers
        if cur_pony and prev_pony and cur_ep == prev_ep and cur_pony != prev_pony:
            if prev_pony in result[cur_pony]:
                result[cur_pony][prev_pony] += 1
            else:
                result[cur_pony][prev_pony] = 1
            
            if cur_pony in result[prev_pony]:
                result[prev_pony][cur_pony] += 1
            else:
                result[prev_pony][cur_pony] = 1

        # update prev
        prev_pony = cur_pony
        prev_ep = cur_ep

    with open(args.output, 'w') as f:
        json.dump(result, f)

if __name__ == '__main__':
    main()
