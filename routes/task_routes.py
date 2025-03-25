from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Task, User
import bleach

task_bp = Blueprint('task_bp', __name__)


@task_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    search_query = request.args.get('search', '')
    search_query = bleach.clean(search_query)

    # Vulnerable to SQL Injection (intentionally insecure)
    if search_query:
        # Using string concatenation for SQL query (intentionally insecure)
        tasks = Task.query.filter(Task.title.like(f'%{search_query}%'), Task.user_id == session['user_id']).all()
    else:
        tasks = Task.query.filter_by(user_id=session['user_id']).all()

    return render_template('dashboard.html', tasks=tasks, search_query=search_query)


@task_bp.route('/task/create', methods=['GET', 'POST'])
def create_task():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        # No input validation for title/description (intentionally insecure)

        new_task = Task(
            title=title,
            description=description,  # Vulnerable to XSS (intentionally insecure)
            user_id=session['user_id']
        )

        db.session.add(new_task)
        db.session.commit()

        flash('Task created successfully!')
        return redirect(url_for('task_bp.dashboard'))

    return render_template('create_task.html')


@task_bp.route('/task/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    task = Task.query.get_or_404(task_id)

    # No check if the task belongs to the current user (intentionally insecure)
    # This allows any user to update any task if they know the task_id

    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.completed = 'completed' in request.form

        db.session.commit()

        flash('Task updated successfully!')
        return redirect(url_for('task_bp.dashboard'))

    return render_template('update_task.html', task=task)