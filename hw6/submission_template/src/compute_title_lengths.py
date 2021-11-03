import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    title_lengths = []
    with open(args.file) as f:
        for line in f:
            post = json.loads(line)
            title_lengths.append(len(post['data']['title']))
    print(sum(title_lengths)//len(title_lengths))

if __name__ == '__main__':
    main()
