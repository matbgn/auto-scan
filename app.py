# Package import
from flask import Flask, render_template, send_file, make_response, url_for, Response, redirect, request
from main import main
from dotenv import load_dotenv
import os

# initialise app
app = Flask(__name__)

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
        main(';'.join(multiselect), request.form['subject'], request.form['scan_mode'],
             request.form['paper_format'], int(request.form['batch_total']), as_web_interface=True, bool(request.form['is_local_scan']))

    return render_template('index.html', mails=emails)


if __name__ == '__main__':
    app.run(debug=True)
