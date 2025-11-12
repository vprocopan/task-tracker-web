from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@login_required
def task_list():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form['title']
    new_task = Task(title=title, owner=current_user)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('tasks.task_list'))

@tasks_bp.route('/toggle/<int:task_id>')
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner == current_user:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('tasks.task_list'))

@tasks_bp.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner == current_user:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('tasks.task_list'))