# Package import
from flask import Flask, render_template, send_file, make_response, url_for, Response, redirect, request
from main import main
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

# initialise app
app = Flask(__name__)

logger.warn("Try to load env...")
load_dotenv()
try:
    emails = os.environ['EMAIL_RECIPIENTS']
except KeyError:
    emails = ""


# decorator for homepage
@app.route('/')
def index():
    return render_template('index.html', mails=emails)


# These functions will run when POST method is used.
@app.route('/', methods=["POST"])
def auto_scan():
    # making sure its not empty
    multiselect = request.form.getlist('email_recipients')
    if request.form['subject'] != '':
        logger.warn("Starts processing 1")

        logger.warn("Param emails: %s",';'.join(multiselect))
        logger.warn("Param subject: %s",request.form['subject'])
        logger.warn("Param mode: %s",request.form['scan_mode'])
        logger.warn("Param format: %s",request.form['paper_format'])
        logger.warn("Param batch: %d",int(request.form['batch_total']))
        logger.warn("Param is_local: %s",request.form['is_local_scan'])

        main(';'.join(multiselect), request.form['subject'], request.form['scan_mode'],
             request.form['paper_format'], int(request.form['batch_total']), as_web_interface=True, is_local_scan=bool(request.form['is_local_scan']))

    return render_template('index.html', mails=emails)


if __name__ == '__main__':
    app.run(debug=True)