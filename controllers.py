"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from py4web.utils.form import Form, FormStyleBulma

import random

@action('index')
@action.uses('index.html', db, auth)
def index():
    rows = db(db.bird).select()
    return dict(
        rows=rows,
    )

def validate_counts(form):
    if form.vars["heard"] > form.vars["number"]:
        form.errors["heard"] = T("You can't have heard more birds than you have detected in total.")


@action('add', method=['GET', 'POST'])
@action.uses('add.html', db, auth.user)
def add():
    form = Form(db.bird, validation=validate_counts, formstyle=FormStyleBulma)
    if form.accepted:
        # The form succeeded, and was processed correctly. The data has been inserted. 
        redirect(URL('index'))
    return dict(
        form=form
    )
 
@action('add-alt', method=['GET', 'POST'])
@action.uses('add.html', db, auth.user)
def add():
    form = Form(db.bird, validation=validate_counts, dbio=False, formstyle=FormStyleBulma)
    if form.accepted:
        # The form succeeded, and was processed correctly. The data has not been inserted. 
        print(f"I should be inserting {form.vars}")
        redirect(URL('index'))
    return dict(
        form=form
    )

    
@action('delete/<bird_id:int>')
@action.uses(db, auth.user)
def delete(bird_id=None):
    assert bird_id is not None
    db((db.bird.id == bird_id) & (db.bird.created_by == get_user_email())).delete()
    redirect(URL('index'))
    
    