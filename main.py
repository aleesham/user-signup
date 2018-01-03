from flask import Flask, redirect, request, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

def is_username_valid(username):
    if len(username) < 3 or len(username) > 20:
        return False
    if ' ' in username:
        return False
    return True

def is_password_valid(password):
    return is_username_valid(password)

def is_verify_password_valid(password, verify_password):
    if password == verify_password:
        return True
    return False

def is_email_valid(email):
    if len(email) == 0:
        return True
    if is_username_valid(email) and email.count('@')*email.count('.') == 1:
        return True
    return False

@app.route('/', methods=['GET','POST'])
def index():
    errors = {'username' : '', 'password': '', 'verify_password': '', 'email' : '' }
    
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        verify_password = request.form['verify_password'].strip()
        email = request.form['email'].strip()
        valid = True                

        if not is_username_valid(username):
            errors['username'] = "This is not a valid username."
            valid = False

        if not is_password_valid(password):
            errors['password'] = "This is not a valid password."
            valid = False

        if not is_verify_password_valid(password, verify_password):
            errors['verify_password'] = "Passwords do not match."
            valid = False

        if not is_email_valid(email):
            errors['email'] = "This is not a valid email."
            valid = False

        if valid:
            return redirect('/welcome?username='+username)
    
        return render_template('signup.html', username=username, email=email, errors = errors)

    return render_template('signup.html', errors=errors)

@app.route('/welcome')
def welcome():
    username = request.args.get('username')
    return render_template('welcome.html',username=username)

app.run()