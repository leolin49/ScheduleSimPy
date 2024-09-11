$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$log_file = "Log\${timestamp}.log"

python main.py
