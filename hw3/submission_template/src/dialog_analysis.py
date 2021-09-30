import sys, argparse, csv, json

# parse cmd-line args
parser = argparse.ArgumentParser()
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument(
    '-o', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
args = parser.parse_args()
in_file = csv.DictReader(args.input_file)
out_file = args.o

ponies = [
    'twilight sparkle',
    'applejack',
    'rarity',
    'pinkie pie',
    'rainbow dash',
    'fluttershy',
]

output = {
    'count':{},
    'verbosity':{}
}

for k in output:
    for pony in ponies:
        output[k][pony] = 0

row_count = 0
for row in in_file:
    row_count += 1
    speaker_ponies = list(filter(lambda s: s in row['pony'].lower(), ponies))
    if speaker_ponies:
        for pony in speaker_ponies:
            output['count'][pony] += 1
            
for pony in ponies:
    output['verbosity'][pony] = output['count'][pony]/row_count

json.dump(output, out_file, indent="")