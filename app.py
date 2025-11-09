#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash
import json, os, threading

app = Flask(__name__)
app.secret_key = "supersecret"  # change in production
TASKS_FILE = "tasks.json"
LOCK = threading.Lock()  # thread safety for concurrent writes


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_tasks(tasks):
    with LOCK:
        with open(TASKS_FILE, "w") as f:
            json.dump(tasks, f, indent=2)


@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    desc = request.form.get("description", "").strip()
    if not desc:
        flash("Task description cannot be empty!", "warning")
        return redirect(url_for("index"))
    tasks = load_tasks()
    tasks.append({"description": desc, "done": False})
    save_tasks(tasks)
    flash("Task added successfully ✅", "success")
    return redirect(url_for("index"))


@app.route("/done/<int:task_id>")
def mark_done(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = True
        save_tasks(tasks)
        flash(f"Marked '{tasks[task_id]['description']}' as done 🎯", "info")
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        removed = tasks.pop(task_id)
        save_tasks(tasks)
        flash(f"Deleted '{removed['description']}' 🗑️", "danger")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777, debug=True)