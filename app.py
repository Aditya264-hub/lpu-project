"""
app.py

System Configuration Comparison Tool
A Python/Tkinter GUI that retrieves a machine's configuration and
compares two configuration snapshots side by side — e.g. two different
computers, or the same computer at two points in time — highlighting
what matches, what differs, and what's missing.

Run with:
    python app.py
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from config_utils import get_system_config, save_config, load_config, compare_configs

APP_TITLE = "System Configuration Comparison Tool"
SNAPSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_configs")

STATUS_COLORS = {
    "same": "#e8f5e9",
    "different": "#fff3e0",
    "only_in_a": "#e3f2fd",
    "only_in_b": "#fce4ec",
}
STATUS_LABELS = {
    "same": "Same",
    "different": "Different",
    "only_in_a": "Only in Config A",
    "only_in_b": "Only in Config B",
}


class ConfigComparisonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("980x560")
        self.minsize(760, 440)

        self.config_a = None
        self.config_b = None
        self.label_a = tk.StringVar(value="Config A: not loaded")
        self.label_b = tk.StringVar(value="Config B: not loaded")
        self.summary_var = tk.StringVar(value="")

        self._build_toolbar()
        self._build_table()
        self._build_statusbar()

    # ---------- UI construction ----------
    def _build_toolbar(self):
        bar = ttk.Frame(self, padding=8)
        bar.pack(fill="x")

        ttk.Button(bar, text="Retrieve Current System -> A",
                   command=self.retrieve_to_a).pack(side="left", padx=4)
        ttk.Button(bar, text="Retrieve Current System -> B",
                   command=self.retrieve_to_b).pack(side="left", padx=4)
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=8)
        ttk.Button(bar, text="Load Snapshot -> A",
                   command=self.load_to_a).pack(side="left", padx=4)
        ttk.Button(bar, text="Load Snapshot -> B",
                   command=self.load_to_b).pack(side="left", padx=4)
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=8)
        ttk.Button(bar, text="Save A as Snapshot",
                   command=lambda: self._save(self.config_a, "A")).pack(side="left", padx=4)
        ttk.Button(bar, text="Save B as Snapshot",
                   command=lambda: self._save(self.config_b, "B")).pack(side="left", padx=4)
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=8)
        ttk.Button(bar, text="Compare A vs B",
                   command=self.compare).pack(side="left", padx=4)

    def _build_table(self):
        frame = ttk.Frame(self, padding=(8, 0, 8, 8))
        frame.pack(fill="both", expand=True)

        columns = ("key", "value_a", "value_b", "status")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.tree.heading("key", text="Setting")
        self.tree.heading("value_a", text="Config A")
        self.tree.heading("value_b", text="Config B")
        self.tree.heading("status", text="Status")
        self.tree.column("key", width=190, anchor="w")
        self.tree.column("value_a", width=290, anchor="w")
        self.tree.column("value_b", width=290, anchor="w")
        self.tree.column("status", width=140, anchor="center")

        for status, color in STATUS_COLORS.items():
            self.tree.tag_configure(status, background=color)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    def _build_statusbar(self):
        bar = ttk.Frame(self, padding=6)
        bar.pack(fill="x")
        ttk.Label(bar, textvariable=self.label_a).pack(side="left", padx=8)
        ttk.Label(bar, textvariable=self.label_b).pack(side="left", padx=8)
        ttk.Label(bar, textvariable=self.summary_var, foreground="#555").pack(side="right", padx=8)

    # ---------- actions ----------
    def retrieve_to_a(self):
        self.config_a = get_system_config()
        self.label_a.set(f"Config A: current system ({self.config_a['hostname']})")
        self._render_single(self.config_a, is_a=True)

    def retrieve_to_b(self):
        self.config_b = get_system_config()
        self.label_b.set(f"Config B: current system ({self.config_b['hostname']})")
        self._render_single(self.config_b, is_a=False)

    def load_to_a(self):
        path = filedialog.askopenfilename(initialdir=SNAPSHOT_DIR,
                                           filetypes=[("JSON snapshot", "*.json")])
        if not path:
            return
        self.config_a = load_config(path)
        self.label_a.set(f"Config A: {os.path.basename(path)}")
        self._render_single(self.config_a, is_a=True)

    def load_to_b(self):
        path = filedialog.askopenfilename(initialdir=SNAPSHOT_DIR,
                                           filetypes=[("JSON snapshot", "*.json")])
        if not path:
            return
        self.config_b = load_config(path)
        self.label_b.set(f"Config B: {os.path.basename(path)}")
        self._render_single(self.config_b, is_a=False)

    def _save(self, config, which):
        if not config:
            messagebox.showwarning(APP_TITLE, f"Retrieve or load Config {which} first.")
            return
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        path = filedialog.asksaveasfilename(
            initialdir=SNAPSHOT_DIR, defaultextension=".json",
            filetypes=[("JSON snapshot", "*.json")])
        if not path:
            return
        save_config(config, path)
        messagebox.showinfo(APP_TITLE, f"Saved Config {which} to {os.path.basename(path)}")

    def compare(self):
        if not self.config_a or not self.config_b:
            messagebox.showwarning(APP_TITLE, "Load or retrieve both Config A and Config B first.")
            return
        rows = compare_configs(self.config_a, self.config_b)
        self._render_rows(rows)
        diffs = sum(1 for r in rows if r[3] != "same")
        self.summary_var.set(f"{len(rows)} settings compared \u00b7 {diffs} difference(s)")

    # ---------- rendering ----------
    def _render_single(self, config, is_a):
        """Show one config on its own, before a comparison has been run."""
        self.tree.delete(*self.tree.get_children())
        for key in sorted(config.keys()):
            row = (key, config[key], "", "") if is_a else (key, "", config[key], "")
            self.tree.insert("", "end", values=row)
        self.summary_var.set("")

    def _render_rows(self, rows):
        self.tree.delete(*self.tree.get_children())
        for key, val_a, val_b, status in rows:
            self.tree.insert("", "end",
                              values=(key, val_a, val_b, STATUS_LABELS[status]),
                              tags=(status,))


if __name__ == "__main__":
    app = ConfigComparisonApp()
    app.mainloop()
