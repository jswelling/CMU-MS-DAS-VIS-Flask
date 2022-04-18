import io
import subprocess
import json
import os
import pandas as pd
from pprint import pprint
from matplotlib.figure import Figure
from matplotlib.backends.backend_svg import FigureCanvasSVG

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

    if 'text' in data and data['text'] != '':
        axes.set_title(data['text'])

@bp.route('/matplotlib_form_submit', methods=['POST'])
def matplotlib_form_submit():
    data = request.get_json()
    print('Request data follows:')
    pprint(data)
    image_holder = io.StringIO()
    # Note that we have to avoid saying 'plt.subplots' because
    # matplotlib.pyplot is not thread-safe. This works, though.
    fig = Figure()
    axes = fig.subplots()
    draw_matplotlib_figure(fig, axes, data)
    FigureCanvasSVG(fig).print_svg(image_holder)
    return {
        #"message":"the ajax exchange happened!",
        "image":image_holder.getvalue()
    }
    

@bp.route('/graphviz_demo')
def graphviz():
    db = get_db()
    return render_template(
        'main/graphviz_demo.html',
        layout_engines=['dot', 'neato', 'twopi', 'circo',
                        'fdp', 'osage', 'patchwork', 'sfdp'
                        ]
    )

@bp.route('/graphviz_form_submit', methods=['POST'])
def graphviz_form_submit():
    data = request.get_json()
    print('in graphviz')
    print('Request data follows:')
    pprint(data)
    if data['out_format'] == 'nolayout':
        # Special case- avoid layout step
        cmd_l = ['neato', '-n2', '-Tsvg']
    else:
        cmd_l = [data['selector'], f"-T{data['out_format']}"]
    rslt = subprocess.run(cmd_l,
                          input=data['textarea'].encode(),
                          capture_output=True)
    pprint(rslt)
    if rslt.returncode:
        return {
            "message": f"An error occurred: {rslt.stderr.decode()}"
            }
    else:
        return {
            #"message":"the ajax exchange happened!",
            "image":rslt.stdout.decode()
        }


def read_class_hierarchy():
    """
    Function to read the D3 class hierarcy example dataset
    """
    this_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(this_dir)
    with open(os.path.join(parent_dir, 'examples', 'd3_classes.json')) as f:
        rslt = json.load(f)
    return rslt


def modify_county_name(row):
    """
    D3 gets confused by things like the city of Butler being in a county of
    the same name, so we append ' Co' to all the county names to make them
    unique.
    """
    return row['County'] + ' Co'


def read_city_info():
    """
    Function to read the city population example dataset
    """
    this_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(this_dir)
    df = pd.read_csv(os.path.join(parent_dir, 'examples', 'PA_cities_counties.tsv'),
                     sep='\t')
    df['parent'] = df.apply(modify_county_name, axis=1)
    df = df[['Name', 'Type', 'parent', 'Class', 'Population (2018 Estimates)',
             'Sq Miles']]
    df = df.rename(columns={'Name': 'name',
                            'Population (2018 Estimates)': 'population',
                            'Sq Miles': 'area',
                            'Type': 'city_or_town',
                            'Class': 'class'})
    rslt = []
    for idx, row in df.iterrows():
        rslt.append(dict(row))
    for elt in df['parent'].unique():
        # add empty records for the counties
        rslt.append({'name': elt, 'parent': 'Pennsylvania'})
    rslt.append({'name': 'Pennsylvania'})
    return rslt
    

#
# Possible sources of data for d3.  In each case:
#   - the key serves as a name for the data source
#   - the value is a tuple containing:
#     - a function to call to get the data dict
#     - the key to use as a value when drawing the hierarchy, e.g. 'population'
#     - 'json' or 'csv', for the format: 'json' means the data is already
#       in a hierarchical representation. 'csv' means the d3 function 'csv'
#
# Every data element is expected to have a 'name' field.  For 'csv' data,
# every element is also expected to have a 'parent' field, which is the
# name of the parent.
#
D3_DATA_SOURCES = {
    'class hierarchy': (read_class_hierarchy, 'size', 'json'),
    'city populations': ( read_city_info, 'population', 'csv'),
}

    
@bp.route('/d3_demo')
def d3():
    db = get_db()
    possible_data_sources = [key for key in D3_DATA_SOURCES]
    return render_template('main/d3_demo.html',
                           data_sources=possible_data_sources)


@bp.route('/d3_form_submit', methods=['POST'])
def d3_form_submit():
    data = request.get_json()
    print('in d3_form_submit')
    print('Request data follows:')
    pprint(data)
    try:
        assert 'selector' in data
        assert data['selector'] in D3_DATA_SOURCES
        fetcher, key, data_type = D3_DATA_SOURCES[data['selector']]
        rslt_data = fetcher()
        print("returning:")
        pprint(rslt_data)
        return {
            #"message":"the ajax exchange happened!",
            "data": rslt_data,
            "key": key,
            "format": data_type
        }
    except Exception as e:
        return {
            "message": f"An error occurred: {e}"
        }
    

