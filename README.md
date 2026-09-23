# System Configuration Comparison Tool

A Python + Tkinter desktop application that retrieves a machine's system
configuration and compares two configuration snapshots side by side —
highlighting what matches, what differs, and what's missing from either
side.

Built as a working prototype (**TRL 3 — Experimental Proof of Concept**)
for the problem statement: *"Develop a Python-based GUI application that
retrieves and compares system configurations."*

## Why this is useful
Labs, colleges and IT teams often need to check whether multiple machines
are configured the same way — same OS version, same RAM, same free disk
space — before rolling out software or running an exam/lab session.
Checking this by hand across many PCs is slow and error-prone. This tool
automates it.

## Features
- **Retrieve** the current machine's configuration: OS, OS version,
  architecture, processor, CPU core count, RAM, disk space, Python
  version, and hostname.
- **Save** any configuration as a reusable JSON snapshot.
- **Load** two saved snapshots (or the live machine plus a saved
  snapshot) into slots A and B.
- **Compare** A vs B in a colour-coded table: matches, differences, and
  settings present in only one config are all flagged separately.

## Screenshots
*Add a screenshot of the running app here after you try it locally —
see "Running it" below.*

## Project structure
```
system-configuration-comparison-tool/
├── app.py                 # Tkinter GUI
├── config_utils.py        # Retrieval, save/load, and comparison logic
├── sample_configs/        # Two example snapshots for a quick demo
│   ├── lab_pc_01.json
│   └── lab_pc_02.json
├── requirements.txt
└── README.md
```

## Running it
```bash
git clone https://github.com/<your-username>/system-configuration-comparison-tool.git
cd system-configuration-comparison-tool
pip install -r requirements.txt
python app.py
```

Then either:
- Click **"Retrieve Current System -> A"**, copy the saved snapshot to
  another PC, retrieve on that PC as B, then compare — or
- Click **"Load Snapshot -> A"** and **"Load Snapshot -> B"** and pick
  the two files in `sample_configs/` for an instant demo, then click
  **Compare A vs B**.

## Tech stack
Python 3 · Tkinter (GUI) · psutil (hardware details) · JSON (snapshot
storage)

## Roadmap
- Export comparison results as a PDF/CSV report
- Compare installed software/package lists, not just hardware and OS
- Remote comparison across networked machines without manual file
  transfer

## Author
Aditya Modi — B.Tech CSE (AI & ML), Lovely Professional University
