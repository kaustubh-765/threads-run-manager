import subprocess
import time
import os
import signal
import json
from datetime import datetime
from pathlib import Path

HOME_DIR = Path.home() / ".taskrunner"
TASKS_FILE = HOME_DIR / "tasks.txt"
PIDS_FILE = HOME_DIR / "pids.json"
CHECK_INTERVALS = 10  # seconds

HOME_DIR.mkdir(parents=True, exist_ok=True)

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
    
def read_tasks():
    if not TASKS_FILE.exists():
        return []
    with open(TASKS_FILE, "r",) as file:
        return [line.strip() for line in file if line.strip() and not line.startswith("#")]
    
def write_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        file.write("\n".join(tasks) + "\n")

def load_pids():
    if not PIDS_FILE.exists():
        return {}
    with open(PIDS_FILE, "r") as file:
        return json.load(file)
    
def save_pids(pids):
    with open(PIDS_FILE, "w") as file:
        json.dump(pids, file)
        
def is_running(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
    
def add_task(cmd):
    tasks = read_tasks()
    if cmd in tasks:
        log("Task already exists")
        return
    tasks.append(cmd)
    write_tasks(tasks)
    log(f"Added task: {cmd}")
    
def remove_task(index):
    tasks = read_tasks()
    if index < 1 or index > len(tasks):
        log("Invalid task index")
        return

    removed = tasks.pop(index-1)
    write_tasks(tasks)
    pids = load_pids()
    if removed in pids and is_running(pids[remove_task]):
        stop_task_by_pid(pids[removed])
        del pids[removed]
        save_pids(pids)
    log(f"Removed task: {removed}")

def list_tasks():
    tasks = read_tasks()
    if not tasks:
        log("No tasks found.")
    else: 
        for i, task in enumerate(tasks):
            print(f"{i} : {task}")
            
def start_task(cmd):
    log(f"Starting task: {cmd}")
    proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
    return proc

def stop_task_by_pid(pid):
    try:
        log(f"Stopping PID: {pid}")
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        os.waitpid(pid, 0)
    except Exception as e:
        log(f"Force killing PID: {pid} -- e: {e}")
        os.killpg(os.getpgid(pid), signal.SIGKILL)
        
def run_monitor():
    tasks = read_tasks()
    pids = load_pids()
    
    # Start only missing tasks
    for cmd in tasks:
        if cmd not in pids or not is_running(pids[cmd]):
            proc = start_task(cmd)
            pids[cmd] = proc.pid
    save_pids(pids)
    
    while True:
        for cmd in tasks:
            pid = pids.get(cmd)
            if not pid or not is_running(pid):
                log(f"Task failed: {cmd}, restarting...")
                proc = start_task(cmd)
                pids[cmd] = proc.pid
                save_pids(pids)
        time.sleep(CHECK_INTERVALS)