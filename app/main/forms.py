from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,SelectField
from wtforms.validators import DataRequired

# Todo Form
class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', render_kw={"rows": 5})
    priority = SelectField('Priority', choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], validators=[DataRequired()])
    submit = SubmitField('Add Todo')


# Edit Form
class EditTodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', render_kw={"rows": 5}) 
    submit = SubmitField('Update Todo')
