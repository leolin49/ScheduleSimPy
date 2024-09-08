#!/bin/bash
timestamp=$(date +"%Y%m%d_%H%M%S")
log_file="Log/${timestamp}.res"
python3 main.py >> "${log_file}"

tail -n 10 bra_event.txt >> "${log_file}"
tail -n 10 lrr_event.txt >> "${log_file}"
tail -n 10 dics_event.txt >> "${log_file}"
tail -n 10 pgcs4ei_event.txt >> "${log_file}"
