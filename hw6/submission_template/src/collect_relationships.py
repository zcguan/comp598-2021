import os
import argparse
import re
import bs4
import json
import requests

BASE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.join(BASE_DIR, '..')

def extract_people_from_a(section, target_person):
    """
    Takes a pageElement and a list of the target person's name breakdown
    Return a list of all people mentioned in link elements identified by what follows "/dating/"
    """
    l = []
    links = section.find_all('a')
    for link in links:
        words = [re.sub(r'\W', '', s.lower())
                 for s in link.find(text=True).split()]
        if words != target_person and r'/dating/' in link['href']:
            l.append(link['href'].strip(r'/dating/'))
    return l

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    
    output = {}
    with open(args.config) as f:
        config = json.load(f)

    CACHE_DIR = os.path.join(PARENT_DIR, config['cache_dir'])
    if not os.path.isdir(CACHE_DIR):
        os.mkdir(CACHE_DIR)
    
    # fetch to cache if not already exists
    for person in config['target_people']:
        output[person] = []
        CACHE_PATH = os.path.join(CACHE_DIR, person+'.html')

        # fetch the page to cache
        if not os.path.isfile(CACHE_PATH):
            response = requests.get(f'https://www.whosdatedwho.com/dating/{person}')
            
            # save to cache
            with open(CACHE_PATH, 'w') as f:
                f.write(response.text)
        
        # use cached file
        with open(CACHE_PATH) as f:
            name = person.split('-')

            soup = bs4.BeautifulSoup(f.read(), 'html.parser')

            # find in status section
            # should have at most one
            status_heading = soup.find('h4', class_='ff-auto-status')
            status = status_heading.next_sibling
            output[person] += extract_people_from_a(status, name)

            # find in relationship section
            relationship_heading = soup.find('h4', class_='ff-auto-relationships')
            current_p = relationship_heading.next_sibling
            while current_p.name == 'p':
                output[person] += extract_people_from_a(current_p, name)
                current_p = current_p.next_sibling

    # write to output file
    with open(args.output, 'w') as f:
        json.dump(output, f)

if __name__ == '__main__':
    main()
