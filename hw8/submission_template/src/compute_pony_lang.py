import argparse
import sys
import json
import math


def main(args=sys.argv[1:], DEBUG=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--counts')
    parser.add_argument('-n', '--num', type=int)
    args = parser.parse_args(args)

    with open(args.counts) as f:
        count = json.load(f)

    total_pony = len(count)

    pony_per_word = {}

    # count nbr of ponies per each word
    for pony in count:
        for w in count[pony]:
            if w in pony_per_word:
                pony_per_word[w] += 1
            else:
                pony_per_word[w] = 1

    result = {}
    # computer tfidf for each word
    for pony in count:
        # max heap to keep only top n
        tfidfHeap = []
        wordHeap = []
        for w in count[pony]:
            idf = math.log10(total_pony/pony_per_word[w])
            tfidf = count[pony][w] * idf
            
            if not tfidfHeap:
                tfidfHeap.append(tfidf)
                wordHeap.append(w)
            else:
                i = 0
                # find index to insert to the heap
                while i < len(tfidfHeap) and i < args.num and tfidf <= tfidfHeap[i]:
                    i += 1
                # if the heap doesnt exceed the max number of words, insert to heap
                if i < args.num:
                    tfidfHeap.insert(i, tfidf)
                    wordHeap.insert(i, w)
                
                # del min if insertion overexpanded the heap
                if len(tfidfHeap) > args.num:
                    del tfidfHeap[-1]
                    del wordHeap[-1]
                    
        result[pony] = wordHeap

    if not DEBUG:
        print(result)
    else:
        return result


if __name__ == '__main__':
    main()
    
