#!/bin/bash
#
timestamp=$(date +"%Y%m%d_%H%M%S")
tar_file="${timestamp}.tar.gz"
cp ./Log/$1 ./
tar -zcvf ${tar_file} bra_event.txt lrr_event.txt dics_event.txt pgcs4ei_event.txt $1
rm -f $1
