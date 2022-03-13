from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from myproj.auth import login_required
from myproj.db import get_db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    return render_template('main/index.html', things=["foo","bar","baz"])

@bp.route('/matplotlib_demo')
def matplotlib():
    db = get_db()
    return render_template('main/matplotlib_demo.html')

@bp.route('/d3_demo')
def d3():
    db = get_db()
    return render_template('main/d3_demo.html')

@bp.route('/graphviz_demo')
def graphviz():
    db = get_db()
    return render_template('main/graphviz_demo.html')
