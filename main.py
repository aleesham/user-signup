from flask import Flask, redirect, render_template, request
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True

## Just renders the form
@app.route('/')
def display_form():
    return render_template('mainform.html')

## helper function to check if a username or password is valid
## invalid if len<3, len>20, or there is a space
def is_valid_string(a_str):
    # returns True if the string is 3-20 characters and has no spaces, returns False otherwise
    return (2 < len(a_str)) & (len(a_str) < 21) & (" " not in a_str)

## Here we will validate everything necessary
@app.route('/', methods=['POST'])
def validate_form():
    # Pull the data from the form
    username = request.form['username']
    pw = request.form['pw']
    verifypw = request.form['verifypw']
    email = request.form['email']

    # initialize errors
    username_error = ''
    pw_error = ''
    verifypw_error = ''
    email_error = ''


    # check if username, pw, or verifypw were left empty
    if not len(username):
        username_error += 'You failed to provide a username.'

    if not len(pw):
        pw_error += 'You failed to provide a password.'

    if not len(verifypw):
        verifypw_error += 'You failed to provide a password verification.'  

    return redirect("/welcome?name=Aleesha")

    # check if the username is valid (write a function for this)

    # check if the password is valid (use function)

    # if no errors, redirect, otherwise re-render with errors
    if not username_error + pw_error + verifypw_error + email_error:
        return redirect("/welcome?name={0}".format(username))
    else:
        return None


## If everything is validated, we will redirect to here.
@app.route('/welcome')
def welcome():
    username = request.args.get('name')
    return render_template('welcome.html', name = username)

app.run()