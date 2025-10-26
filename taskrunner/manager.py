import subprocess
import time
import os
import signal
import json
from datetime import datetime
from pathlib import Path
from filelock import FileLock

HOME_DIR = Path.home() / ".taskrunner"
TASKS_FILE = HOME_DIR / "tasks.txt"
PIDS_FILE = HOME_DIR / "pids.json"
TASKS_LOCK = HOME_DIR / "tasks.lock"
PIDS_LOCK = HOME_DIR / "pids.lock"
CHECK_INTERVALS = 10  # seconds

HOME_DIR.mkdir(parents=True, exist_ok=True)

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
    
def read_tasks():
    with FileLock(TASKS_LOCK):
        if not TASKS_FILE.exists():
            return []
        with open(TASKS_FILE, "r",) as file:
            return [line.strip() for line in file if line.strip() and not line.startswith("#")]
    
def write_tasks(tasks):
    with FileLock(TASKS_LOCK):
        with open(TASKS_FILE, "w") as file:
            file.write("\n".join(tasks) + "\n")

def load_pids():
    with FileLock(PIDS_LOCK):
        if not PIDS_FILE.exists():
            return {}
        with open(PIDS_FILE, "r") as file:
            return json.load(file)
    
def save_pids(pids):
    with FileLock(PIDS_LOCK):
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
    if removed in pids:
        if is_running(pids[removed]):
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
    try:
        proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
        return proc
    except Exception as e:
        log(f"Failed to start task '{cmd}': {e}")
        return None

def stop_task_by_pid(pid):
    try:
        log(f"Stopping PID: {pid}")
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        os.waitpid(pid, 0)
    except Exception as e:
        log(f"Force killing PID: {pid} -- e: {e}")
        os.killpg(os.getpgid(pid), signal.SIGKILL)
        
import signal

_stop_monitor = False

def _signal_handler(signum, frame):
    global _stop_monitor
    log(f"Signal {signum} received, stopping monitor...")
    _stop_monitor = True

def run_monitor():
    global _stop_monitor
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    while not _stop_monitor:
        tasks = read_tasks()
        pids = load_pids()
        
        # Start only missing tasks
        for cmd in tasks:
            if cmd not in pids or not is_running(pids[cmd]):
                proc = start_task(cmd)
                if proc:
                    pids[cmd] = proc.pid
                else:
                    # If task failed to start, remove it from pids to avoid trying to monitor it
                    if cmd in pids:
                        del pids[cmd]
        save_pids(pids)
        
        for cmd in tasks:
            pid = pids.get(cmd)
            if not pid or not is_running(pid):
                log(f"Task failed: {cmd}, restarting...")
                proc = start_task(cmd)
                if proc:
                    pids[cmd] = proc.pid
                else:
                    # If task failed to restart, remove it from pids
                    if cmd in pids:
                        del pids[cmd]
                save_pids(pids)
        time.sleep(CHECK_INTERVALS)