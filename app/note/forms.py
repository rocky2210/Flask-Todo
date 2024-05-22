from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import SubmitField,StringField
from wtforms.validators import DataRequired

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField('Save')
