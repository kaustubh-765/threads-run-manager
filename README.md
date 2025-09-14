# TaskRunner 🛠️

**TaskRunner** is a lightweight CLI tool for managing long-running background tasks.  
It lets you define commands in a task file, automatically monitor them, and restart them if they fail — ensuring your workflows keep running with minimal overhead.  

---

## ✨ Features
- Add, list, and remove tasks via the command line.
- Run and monitor background tasks.
- Restart failed processes automatically (prevents zombie tasks).
- PID tracking for clean process management.
- Cross-platform (Linux & macOS).
- Uses minimal memory & CPU by recycling failed processes.

---

## 📦 Installation

Clone the repository and install with `pip`:

```bash
git clone https://github.com/yourusername/taskrunner.git
cd taskrunner

# Development mode (recommended during setup)
pip install -e .

---

## ✅ Verify Installation

Run:

```bash
which taskrunner

⚡ Usage
➕ Add a new task
```bash
taskrunner add "ping google.com"