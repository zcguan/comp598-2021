import requests
import argparse
import json
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.join(BASE_DIR, '..')
ENV_PATH = os.path.join(PARENT_DIR, '.env')

load_dotenv(ENV_PATH)

def auth():
    client_auth = requests.auth.HTTPBasicAuth(
        'wv_Qxb6mWPK6uCWGjCLH2A', '-ukkpThagRHdtlcXpVEOSVNRrEqSzw')
    post_data = {'grant_type': 'password',
                 'username': os.environ.get("REDDIT_USER"),
                 'password': os.environ.get("REDDIT_PWD")}

    headers = {'User-Agent': 'myapp/0.0.1'}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

    TOKEN = response.json()['access_token']

    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    return headers

def collect_posts(fname, subreddit, headers, limit):
    with open(fname, 'w') as f:
        response = requests.get(
            f'https://oauth.reddit.com{subreddit}/new', headers=headers, params={'limit': limit})
        for post in response.json()['data']['children']:
            f.write(json.dumps(post) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-s', '--subreddit')

    args = parser.parse_args()

    header = auth()
    
    if os.path.dirname(args.output):
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    collect_posts(args.output, args.subreddit.strip(), header, 100)

if __name__ == '__main__':
    main()
