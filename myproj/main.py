import io
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure

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

def draw_matplotlib_figure(fig, axes, data):
    axes.plot([0.0, 1.0, 2.0, 3.0], [0.0, 1.0, 4.0, 9.0])

    if 'axes_cbox' in data and not data['axes_cbox']:
        # Hide the right and top spines
        axes.spines['right'].set_visible(False)
        axes.spines['top'].set_visible(False)

        # Only show ticks on the left and bottom spines
        axes.yaxis.set_ticks_position('left')
        axes.xaxis.set_ticks_position('bottom')
        
    if 'log_cbox' in data and data['log_cbox']:
        axes.set_yscale('log')

@bp.route('/matplotlib_form_submit', methods=['POST'])
def matplotlib_form_submit():
    data = request.get_json()
    print('Request data follows:')
    pprint(data)
    image_holder = io.StringIO()
    fig, axes = plt.subplots()
    draw_matplotlib_figure(fig, axes, data)
    FigureCanvasSVG(fig).print_svg(image_holder)
    return {
        #"message":"the ajax exchange happened!",
        "image":image_holder.getvalue()
    }
    

@bp.route('/d3_demo')
def d3():
    db = get_db()
    return render_template('main/d3_demo.html')

@bp.route('/graphviz_demo')
def graphviz():
    db = get_db()
    return render_template('main/graphviz_demo.html')
