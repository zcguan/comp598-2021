#!/bin/bash

# need input file and output file as args
if [ -z "$2" ]
then
        echo "Need two arguments"
        exit 1
fi

# match all lines that starts with 8 digits followed by a comma and a date ending with 2020
grep -P "^\d{8}\,\d{2}\/\d{2}\/2020" $1 > $2