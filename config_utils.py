"""
config_utils.py

Core logic for the System Configuration Comparison Tool.
Kept separate from the GUI (app.py) so it can be tested, reused, or
swapped onto a different interface without touching the Tkinter code.
"""

import json
import os
import platform
import socket
from datetime import datetime

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def get_system_config():
    """Collect a snapshot of the current machine's configuration."""
    config = {
        "snapshot_taken_at": datetime.now().isoformat(timespec="seconds"),
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor() or "Unknown",
        "python_version": platform.python_version(),
    }

    if HAS_PSUTIL:
        config["cpu_cores_physical"] = psutil.cpu_count(logical=False)
        config["cpu_cores_logical"] = psutil.cpu_count(logical=True)
        config["total_ram_gb"] = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        config["available_ram_gb"] = round(psutil.virtual_memory().available / (1024 ** 3), 2)
        disk = psutil.disk_usage(os.path.abspath(os.sep))
        config["total_disk_gb"] = round(disk.total / (1024 ** 3), 2)
        config["free_disk_gb"] = round(disk.free / (1024 ** 3), 2)
    else:
        config["cpu_cores_physical"] = "psutil not installed"
        config["cpu_cores_logical"] = os.cpu_count()
        config["total_ram_gb"] = "psutil not installed"
        config["available_ram_gb"] = "psutil not installed"
        config["total_disk_gb"] = "psutil not installed"
        config["free_disk_gb"] = "psutil not installed"

    return config


def save_config(config, filepath):
    """Write a configuration dict to disk as JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def load_config(filepath):
    """Read a configuration snapshot back from disk."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def compare_configs(config_a, config_b):
    """
    Compare two configuration dictionaries.

    Returns a list of tuples: (key, value_a, value_b, status)
    where status is one of "same", "different", "only_in_a", "only_in_b".
    """
    keys = sorted(set(config_a.keys()) | set(config_b.keys()))
    rows = []
    for key in keys:
        in_a = key in config_a
        in_b = key in config_b
        if in_a and in_b:
            status = "same" if config_a[key] == config_b[key] else "different"
            rows.append((key, config_a[key], config_b[key], status))
        elif in_a:
            rows.append((key, config_a[key], "-", "only_in_a"))
        else:
            rows.append((key, "-", config_b[key], "only_in_b"))
    return rows
