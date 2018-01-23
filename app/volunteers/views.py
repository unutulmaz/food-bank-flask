#app/volunteers/views.py
from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.models import Volunteer
from app.forms import VolunteerForm
from app.errors import *
from app import db
from sqlalchemy import exc
from app.login_helpers import *

volunteers_blueprint = Blueprint('volunteers', __name__, template_folder='templates')

@volunteers_blueprint.route('/', methods=['GET', 'POST'])
@admin_logged_in
def index():
    if request.method == 'POST':
        volid = request.form['id']
        volunteer = Volunteer.query.get(volid)
        if request.form['submit'] == 'Mark Active':
            volunteer.active = True
            flash('Volunteer %s status changed to Active' % volunteer.name, 'success')
        elif request.form['submit'] == 'Mark Inactive':
            volunteer.active = False
            flash('Status of %s changed to Inactive' % volunteer.name, 'success')

        db.session.commit()
        return redirect(url_for('volunteers.index'))

    elif request.method == 'GET':
        volunteers = Volunteer.query.order_by(Volunteer.name.asc()).all()
        if volunteers:
            return render_template('volunteers.html', volunteers=volunteers)
        else:
            msg = 'No Volunteers Found'
            return render_template('volunteers.html', msg=msg)

@volunteers_blueprint.route('/new', methods=['GET', 'POST'])
@admin_logged_in
def new_volunteer():
    form = VolunteerForm(request.form)
    if request.method == 'POST' and form.validate():
        new_volunteer = Volunteer(
            name = form.name.data,
            email = form.email.data,
            role = form.role.data,
            active = True
        )

        db.session.add(new_volunteer)
        db.session.commit()
        # try:
        #     db.session.add(new_volunteer)
        #     db.session.commit()
        # except exc.SQLAlchemyError:
        #     return '<h1>NOPE</h1>'

        flash('Volunteer %s added!' % new_volunteer.name, 'success')

        return redirect(url_for('volunteers.index'))
    return render_template('volunteer_form.html', form=form)

@volunteers_blueprint.route('/<string:id>/edit', methods=['GET', 'POST'])
@admin_logged_in
def edit_volunteer(id):

    volunteer = Volunteer.query.get(id)
    form = VolunteerForm(request.form, obj=volunteer)

    if request.method == 'POST' and form.validate():

        form.populate_obj(volunteer)

        db.session.commit()

        flash('Information for %s Updated' % volunteer.name, 'success')

        return redirect(url_for('index'))
    else:
        return render_template('volunteer_form.html', form=form)

# @volunteers_blueprint.route('/<string:id>/edit_status', methods=['POST'])
# @admin_logged_in
def edit_status(id):
    volunteer = Volunteer.query.get(id)

    if volunteer.active == True:
        volunteer.active = False
    else:
        volunteer.active = True

    db.session.commit()
    flash('Volunteer %s status changed' % volunteer.name, 'success')

    return redirect(url_for('volunteers'))
