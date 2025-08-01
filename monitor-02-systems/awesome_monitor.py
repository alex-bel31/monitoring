#!/usr/bin/env python3

import time
import json
from datetime import datetime

LOG_DIR = '/var/log'
DATE_FMT = '%y-%m-%d'
FILENAME = f"{datetime.now().strftime(DATE_FMT)}-awesome-monitoring.log"
LOG_PATH = f"{LOG_DIR}/{FILENAME}"

def get_metrics():
    metrics = {}
    metrics['timestamp'] = int(time.time())

    # CPU load 
    with open('/proc/stat', 'r') as f:
        cpu_line = f.readline().split()
        user, nice, system = int(cpu_line[1]), int(cpu_line[2]), int(cpu_line[3])
        metrics['cpu_user'] = user
        metrics['cpu_system'] = system

    # Memory
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
        mem_total = int(lines[0].split()[1])
        mem_free = int(lines[1].split()[1])
        metrics['mem_total_kb'] = mem_total
        metrics['mem_free_kb'] = mem_free

    # Process count
    with open('/proc/loadavg', 'r') as f:
        load_avg = f.read().split()
        metrics['loadavg_1min'] = float(load_avg[0])

    return metrics

def write_log(metrics):
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(metrics) + '\n')

if __name__ == '__main__':
    metrics = get_metrics()
    write_log(metrics)
