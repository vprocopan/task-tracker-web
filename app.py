#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
TASKS_FILE = "tasks.json"


# ──────────────────────────────────────────────
# Utility functions
# ──────────────────────────────────────────────
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────
@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    tasks = load_tasks()
    desc = request.form.get("description")
    if desc:
        tasks.append({"description": desc, "done": False})
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/done/<int:task_id>")
def mark_done(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = True
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7777)