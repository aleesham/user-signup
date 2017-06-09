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
def is_valid_text(a_str):
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


    # check if username was left empty or is invalid
    if not len(username):
        username_error = 'You failed to provide a username. '
    elif not is_valid_text(username):
        username_error = 'You entered an invalid username.'

    # check if password was left empty or is invalid    
    if not len(pw):
        pw_error = 'You failed to provide a password.'
    elif not is_valid_text(pw):
        pw_error = 'You entered an invalid password.'

    # check if verified password was left empty or if it matches password
    if not len(verifypw):
        verifypw_error = 'You failed to provide a password verification.'     
    elif pw != verifypw:
        verifypw_error = 'These passwords do not match.'

    # if email provided, check validity.
    if len(email):
        # check length and spaces
        length_and_spaces_bool = is_valid_text(email)
        # check for @, assume False at first.
        at_and_dot_bool = False
        # if there are an at and dot in the email, then check to make sure there are exactly one of each. if there isn't, then at_and_dot_bool stays False.
        if "@" in email and "." in email:
            # if there are exactly one of each, then at_and_dot_bool is true. If not, at_and_dot_bool stays false
            if email.count("@") == 1 and email.count(".") == 1:
                at_and_dot_bool = True

        # if the length and spaces are not met, or the at and dot are not met, we throw an error
        if not length_and_spaces_bool or not at_and_dot_bool:
            email_error = 'You have entered an invalid email.'   

    # if no errors, redirect, otherwise re-render with errors
    if not username_error + pw_error + verifypw_error + email_error:
        return redirect("/welcome?name={0}".format(username))
    else:
        return render_template('mainform.html', username_error = username_error, pw_error = pw_error, verifypw_error = verifypw_error, email_error = email_error, username = username, email = email)


## If everything is validated, we will redirect to here.
@app.route('/welcome')
def welcome():
    username = request.args.get('name')
    return render_template('welcome.html', name = username)

app.run()