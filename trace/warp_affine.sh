#!/bin/sh
for file in ./source/output*.bmp
do
    echo $file
    ./perspective_transform.o $file
done
