#/bin/bash
kill -9 `cat /run/scan_dir.pid`
nohup python scan_dir.py >/dev/null 2>&1 &