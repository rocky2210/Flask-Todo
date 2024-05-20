from flask import Blueprint, render_template, redirect, url_for, flash,request
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import Todo
from app.main.forms import TodoForm, EditTodoForm


@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/about')
def about():
    return render_template('main/about.html')

@bp.route('/faq')
def faq():
    return render_template('main/FAQs.html')


# Todo Route
@bp.route('/todos')
@login_required
def todos():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    name = current_user.username
    return render_template('main/todos.html',todos=todos,name=name )


# Add Todo Route
@bp.route('/add_todo',methods=['GET','POST'])
@login_required
def add_todo():
    form = TodoForm()
    if form.validate_on_submit():
        priority = request.form.get('priority')
        todo = Todo(
            title=form.title.data,
            description=form.description.data,
            priority=priority, 
            user_id=current_user.id
            )
        db.session.add(todo)
        db.session.commit()
        flash('Todo added Successfully','success')
        return redirect(url_for('main.todos'))
    return render_template('main/add_todo.html',form=form)


# Delete todo
@bp.route('/delete_todo/<int:todo_id>', methods=['POST'])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash("Todo deleted Successfully",'danger')
    return redirect(url_for('main.todos'))


#Edit Todo Route
@bp.route('/edit_todo/<int:todo_id>',methods=['GET','POST'])
@login_required
def edit_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        flash('Todo not found', 'error')
        return redirect(url_for('main.todo'))
    form = EditTodoForm(obj=todo)
    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        db.session.commit()
        flash('Todo updated successfully', 'success')
        return redirect(url_for('main.todos'))
    return render_template('main/update.html', form=form)


# Completed route
@bp.route('/complete_todo/<int:todo_id>', methods=['POST'])
@login_required
def complete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == current_user.id:
        if todo.completed:
            todo.completed = False
            flash("Todo marked as incomplete", 'warning')
        else:
            todo.completed = True
            flash("Todo marked as completed", 'success')
        db.session.commit()
    return redirect(url_for('main.todos'))