# Package import
from flask import Flask, render_template, send_file, make_response, url_for, Response, redirect, request
from main import main

# initialise app
app = Flask(__name__)


# decorator for homepage
@app.route('/')
def index():
    return render_template('index.html',
                           PageTitle="Landing page")


# These functions will run when POST method is used.
@app.route('/', methods=["POST"])
def auto_scan():
    # making sure its not empty
    if request.form['subject'] != '':
        main(request.form['email_recipients'], request.form['subject'], request.form['scan_mode'],
             request.form['paper_format'], int(request.form['batch_total']))

    return render_template('index.html',
                           PageTitle="Landing page")
    # This just reloads the page if no file is selected and the user tries to POST.


if __name__ == '__main__':
    app.run(debug=True)
