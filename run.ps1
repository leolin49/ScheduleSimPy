$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$log_file = "Log\${timestamp}.log"
python main.py > $log_file

Get-Content bra_event.txt -Tail 10 >> $log_file
Get-Content lrr_event.txt -Tail 10 >> $log_file
Get-Content dics_event.txt -Tail 10 >> $log_file
Get-Content pgcs4ei_event.txt -Tail 10 >> $log_file