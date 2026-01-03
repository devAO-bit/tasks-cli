#!/usr/bin/env python3

import sys
import json
import os
from datetime import datetime

FILE_NAME = 'tasks.json'

# ------------Utility Function--------------
def ensure_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w') as f:
            json.dump([], f, indent=2)

def read_tasks():
    ensure_file()
    with open(FILE_NAME, 'r') as f:
        return json.load(f)
    
def write_tasks(tasks):
    with open(FILE_NAME, 'w') as f:
        json.dump(tasks, f, indent=2)

def generate_id(tasks):
    return max((task["id"] for task in tasks), default=0) + 1

def current_time():
    return datetime.now().isoformat(timespec="seconds")
