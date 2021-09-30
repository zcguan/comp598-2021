#!/bin/bash

file=$1

wc=$(wc -l < $file)

if [ $wc -lt 10000 ]
then
    echo "ERROR: the input file is smaller than 10,000 lines."
else
    echo $wc
    head $file -n 1
    tail -n 10000 $file | grep -i -c potus
    head -n 200 $file | tail -n 100 | grep "\bfake\b" -c
fi
