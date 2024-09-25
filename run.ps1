$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$log_file = "Log\${timestamp}.log"

python main.py

# 性能分析
python -m cProfile -o profile_file.prof main.py

snakeviz .\profile_file.prof

