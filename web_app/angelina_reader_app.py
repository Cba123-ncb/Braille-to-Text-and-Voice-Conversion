#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
web application Braille Reader
"""
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, FileField, TextAreaField, HiddenField
from wtforms.validators import DataRequired
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template

import atexit
from email.mime.text import MIMEText
import time
import json
import signal
import sys
import argparse
import uuid
from pathlib import Path
import socket

from .config import Config
from .angelina_reader_core import AngelinaSolver, VALID_EXTENTIONS, fill_message_headers, send_email


def startup_logger():
    hostname = socket.gethostname()
    def send_startup_email(what):
        """
        """
        # For local development, just print instead of sending email
        print(f'Braille Reader is {what} at {hostname}')
        return
        # create message object instance
        txt = 'Braille Reader is {} at {}'.format(what, hostname)
        msg = fill_message_headers(MIMEText(txt, _charset="utf-8"), 'Braille Reader<admin@braille-reader.com>', txt)
        send_email(msg)

    send_startup_email('started')

    atexit.register(send_startup_email, 'stopped')
    def signal_handler(sig, frame):
        send_startup_email('interrupted by caught {}'.format(sig))
        sys.exit(0)
    for s in set(signal.Signals):
        try:
            signal.signal(s, signal_handler)
        except:
            print('failed to set handler for signal {}'.format(s))

app = Flask(__name__)
Mobility(app)
app.config.from_object(Config)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

data_root_path = Path(app.root_path) / app.config['DATA_ROOT']

core = AngelinaSolver(data_root_path=data_root_path)


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@mobile_template('{m/}index.html')
def index(template, is_mobile=False):
    class MainForm(FlaskForm):
        file = FileField('Upload Braille Image')
        submit = SubmitField('Recognize Text')
    
    form = MainForm()
    
    if form.validate_on_submit():
        file_data = form.file.data
        if not file_data:
            flash('Please upload a file')
            return render_template(template, form=form)
        
        filename = file_data.filename
        file_ext = Path(filename).suffix.lower()
        if file_ext not in VALID_EXTENTIONS:
            flash('Invalid file type {}: {}'.format(file_ext, filename))
            return render_template(template, form=form)

        # Generate a simple user ID for non-authenticated use
        import uuid
        user_id = str(uuid.uuid4())
        
        extra_info = {
            'user': user_id,
            'has_public_confirm': False,  # Default to "I object"
            'lang': 'EN',  # English only
            'find_orientation': True,  # Auto-orientation enabled by default
            'process_2_sides': False,
        }
        
        task_id = core.process(user_id=user_id, file_storage=file_data, param_dict=extra_info)
        
        return redirect(url_for('results', task_id=task_id))

    return render_template(template, form=form)


@app.route("/results")
@mobile_template('{m/}results.html')
def results(template):
    task_id = request.args.get('task_id')
    if not task_id:
        flash('No task ID provided')
        return redirect(url_for('index'))
    
    if not core.is_completed(task_id, timeout=1):
        flash('Processing not completed or failed')
        return redirect(url_for('index'))
    
    results_list = core.get_results(task_id)
    if results_list is None:
        flash('Error processing file. Please check file format and try again.')
        return redirect(url_for('index'))
    
    # Convert OS path to flask html path
    image_paths_and_texts = list()
    for marked_image_path, recognized_text_path, recognized_braille_path in results_list["item_data"]:
        # Full path to image -> "/static/..."
        marked_image_path = marked_image_path[1:]
        marked_image_path = str(Path(marked_image_path).relative_to(app.config['DATA_ROOT']))
        recognized_text_path = str(Path(recognized_text_path).relative_to(data_root_path))

        with open(data_root_path / recognized_text_path, encoding="utf-8") as f:
            out_text = ''.join(f.readlines())
        
        image_paths_and_texts.append(("/" + app.config['DATA_ROOT'] + "/" + marked_image_path, out_text))

    return render_template(template, image_paths_and_texts=image_paths_and_texts)

@app.route("/help")
def help():
    return render_template('help.html')


@app.route("/results_demo")
@mobile_template('{m/}results_demo.html')
def results_demo(template):
    time.sleep(1)
    return render_template(template)


@app.route("/donate", methods=['GET', 'POST'])
@mobile_template('{m/}donate.html')
def donate(template):
    return render_template(template)


def run():
    parser = argparse.ArgumentParser(description='Braille Reader web app.')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='enable debug mode (default: off)')
    args = parser.parse_args()
    debug = args.debug
    if not debug:
        startup_logger()
    if debug:
        print('running in DEBUG mode!')
    else:
        print('running with no debug mode')
    app.jinja_env.cache = {}
    if debug:
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(debug=True, host='0.0.0.0', port=5001)
    else:
        app.run(host='0.0.0.0', port=5001, threaded=True)

if __name__ == "__main__":
    run()