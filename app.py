from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_migrate import Migrate

# Create a Flask instance
app = Flask(__name__)

# Add mysql database configuration
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:@localhost/flasktodo' # Database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CSRF TOKEN
app.config['SECRET_KEY'] = "Thisismysecretkey"

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# User model
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250))
    completed = db.Column(db.Boolean,default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

# Todo Form
class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', render_kw={"rows": 5}) 
    submit = SubmitField('Add Todo')


# Edit Form
class EditTodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', render_kw={"rows": 5}) 
    submit = SubmitField('Update Todo')


# Add Todo Route
@app.route('/add_todo',methods=['GET','POST'])
@login_required
def add_todo():
    form = TodoForm()
    if form.validate_on_submit():
        todo = Todo(title=form.title.data,description=form.description.data, user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        flash('Todo added Successfully','success')
        return redirect(url_for('todos'))
    
    return render_template('add_todo.html',form=form)

# Todo Route
@app.route('/todos')
@login_required
def todos():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    name = current_user.username
    return render_template('todos.html',todos=todos,name=name )


# Delete todo
@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash("Todo deleted Successfully",'danger')
    return redirect(url_for('todos'))


#Edit Todo Route
@app.route('/edit_todo/<int:todo_id>',methods=['GET','POST'])
@login_required
def edit_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        flash('Todo not found', 'error')
        return redirect(url_for('todo'))
    form = EditTodoForm(obj=todo)
    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        db.session.commit()
        flash('Todo updated successfully', 'success')
        return redirect(url_for('todos'))
    else :
        flash('Some issues', 'danger')
    return render_template('update.html', form=form)

# Login Route
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # Checking hash
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Login Successfully")
                return redirect(url_for('todos'))
            else:
                flash("Wrong Password - Try Again")
        else:
            flash("That user not exist")
    return render_template('login.html',form=form)

# Register Route
@app.route('/register',methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! Your are now able to log in.",'success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout successfully")
    return redirect(url_for('login'))


# Completed route
@app.route('/complete_todo/<int:todo_id>', methods=['POST'])
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
    return redirect(url_for('todos'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('FAQs.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)

