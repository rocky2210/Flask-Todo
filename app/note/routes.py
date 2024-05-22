from flask import render_template,flash,redirect,url_for,request
from flask_login import current_user,login_required
from app import db
from app.models import Note
from app.note.forms import NoteForm
from app.note import bp
# from flask_security.utils import mark_safe


@bp.route('/notes')
@login_required
def notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('note/notes.html',notes=notes)


# Add Route
@bp.route('/add_note',methods=['GET','POST'])
@login_required
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data,content=form.content.data,user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        flash('Note added successfully','success')
        return redirect(url_for('note.notes'))
    return render_template('note/add_note.html',form=form)


# View notes
@bp.route('/view_note/<int:note_id>', methods=['GET'])
@login_required
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    # note.content = mark_safe(note.content)
    if note.user_id != current_user.id:
        flash('You do not have permission to view this note', 'danger')
        return redirect(url_for('note.notes'))
    return render_template('note/note.html', note=note)


# Delete note
@bp.route('/delete_note/<int:note_id>',methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note.user_id != current_user.id:
        flash('You do not have permission to delete this note', 'danger')
        return redirect(url_for('note.notes'))
    if note:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted successfully",'danger')
    return redirect(url_for('note.notes'))


# Edit note
@bp.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if not note:
        flash('Todo not found', 'danger')
        return redirect(url_for('note.notes'))
    
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Note updated successfully', 'success')
        return redirect(url_for('note.notes'))
    return render_template('note/update_note.html', form=form)