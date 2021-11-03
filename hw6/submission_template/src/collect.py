import os
import json
import requests
import requests.auth
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.join(BASE_DIR, '..')
SAMPLE1 = os.path.join(PARENT_DIR, 'sample11.json')
SAMPLE2 = os.path.join(PARENT_DIR, 'sample22.json')
ENV_PATH = os.path.join(PARENT_DIR, '.env')

load_dotenv(ENV_PATH)

SAMPLE1_SUBREDDITS = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews', 'videos', 'todayilearned']
SAMPLE2_SUBREDDITS = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers', 'PublicFreakout', 'leagueoflegends', 'unpopularopinion']

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

def collect_posts(fname, subreddit_list, headers, limit):
    with open(fname, 'w') as f:
        # json.dump(response.json(), f)
        for subr in subreddit_list:
            response = requests.get(
                f'https://oauth.reddit.com/r/{subr}/new', headers=headers, params={'limit':limit})
            for post in response.json()['data']['children']:
                f.write(json.dumps(post) + '\n')
            
def main():
    headers = auth()

    # response = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    # response = requests.get('https://oauth.reddit.com/r/funny/new', headers=headers)

    
    # with open(SAMPLE1, 'w') as f:
    #     # json.dump(response.json(), f)
    #     for subr in SAMPLE1_SUBREDDITS:
    #         response = requests.get(f'https://oauth.reddit.com/r/{subr}/new', headers=headers)
    #         for i in range(100):
    #             f.write(json.dumps(response.json()['data']['children'][i]) + '\n')

    collect_posts(SAMPLE1, SAMPLE1_SUBREDDITS, headers, 100)
    collect_posts(SAMPLE2, SAMPLE2_SUBREDDITS, headers, 100)


if __name__ == '__main__':
    main()
