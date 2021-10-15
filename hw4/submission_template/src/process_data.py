"""
From the 1,2,8 th column of the 2020 data, compute the average monthly incident create-to-closed time (in hours) and save the result for all data, and for each zipcode, as well as a list of zipcodes for bokeh dashboard.

"""

import pandas as pd
import os.path
import argparse

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')

    args = parser.parse_args()

    inputFile = os.path.join(DATA_DIR, 'trimmed_data.csv')
    if args.input:
        inputFile = args.input

    # keep only creation, close date, and zip code
    df = pd.read_csv(inputFile, parse_dates=[1, 2], usecols=[1,2,8], header=None)
    unique_zip = df[8].nunique()
    # print(unique_zip)
    
    # remove not yet closed and missing zip
    df = df[df[2].notnull() & df[8].notnull()]
    df = pd.concat([df, df[2]-df[1]], axis=1)
    df.columns = ['start', 'end', 'zip', 'delta']
    # convert delta to hours
    df['delta'] = df['delta'].map(lambda d: d.total_seconds()/3600)
    # remove negative delta
    df = df[df['delta'] >= 0]
    # convert zip to int
    df['zip'] = df['zip'].astype(int)
    # take only the ending month
    df['end'] = df['end'].map(lambda d: d.month)
    
    # all data monthly avg
    df_avg = df.groupby('end').mean()
    df_avg = df_avg.drop(columns=['zip'])
    df_avg.to_csv(os.path.join(DATA_DIR, 'all.csv'))
    
   
    # per zip
    df = df[['end','zip','delta']]
    with open(os.path.join(DATA_DIR, 'zip.txt'), 'w') as f:
        for zip, df_zip in df.groupby('zip'):
            f.write(f'{zip} ')
            df_avg = df_zip.groupby('end').mean()
            df_avg = df_avg.drop(columns=['zip'])

            df_avg.to_csv(os.path.join(DATA_DIR, f'{zip}.csv'))


    # print(df)

if __name__ == '__main__':
    main()
