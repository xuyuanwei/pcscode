#!/bin/sh
for file in ./source/output*.bmp
do
    echo $file
    ./test.o $file
done
