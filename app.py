from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from functools import wraps
import backend.backend_functions as backend_functions
import os
import re

app = Flask(__name__, template_folder='frontend/html', static_folder='static')
secret_key = os.urandom(12).hex()
app.secret_key = secret_key


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'username' not in session:

            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    
    return decorated_function


@app.route('/')
def index():
    
    return render_template('telaInicial.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
            
        # Get the user's input from the registration form
        full_name = request.form.get('FullName')
        phone_number = request.form.get('PhoneNumber')
        email = request.form.get('Email')

        formatted_phone_number = re.sub(r'[\(\)\-\s]', '', phone_number)

        if request.form.get('Password') != '' and email != '':

            # Hash the password
            hashed_password = backend_functions.hash_password(request.form.get('Password'))

            # Save the username and hashed password in the database
            backend_functions.save_to_database(full_name, formatted_phone_number, email, hashed_password)

        # Redirect to the home page
        return redirect('/')
    
    elif request.method == 'GET':

        return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('Email')

        if request.form.get('Password') != '' and email != '':

            match, username, user_hash = backend_functions.check_login_credentials(email, request.form.get('Password'))

            if match:

                session['username'] = username
                session['user_hash'] = user_hash
                passwords = backend_functions.fetch_passwords(user_hash)

                # Store the passwords in a session variable
                session["passwords"] = passwords

                # Redirect to the route that displays the passwords
                return redirect(url_for("dashboard"))
            
            else:
                
                return redirect('/')

    elif request.method == 'GET':

        return render_template('login.html')
    

@app.route('/passwords')
@login_required
def dashboard():

    user_hash = session.get('user_hash')

    passwords = session.get("passwords") or backend_functions.fetch_passwords(user_hash)

    return render_template('senhasCadastradas.html', passwords=passwords)


@app.route('/new_password', methods=['GET', 'POST'])
@login_required
def new_password():

    if request.method == 'POST':

        user_hash = session.get('user_hash')

        origin_url = request.form.get('originURL')
        origin_name = request.form.get('originName')
        origin_password = request.form.get('originPassword')

        backend_functions.add_new_password(user_hash, origin_url, origin_name, origin_password)

        # Fetch the updated passwords from the database
        passwords = backend_functions.fetch_passwords(user_hash)
        session['passwords'] = passwords

        return redirect('/passwords')

    elif request.method == 'GET':

        return render_template('adicionarNovasSenhas.html')
    

@app.route('/delete_password', methods=['POST'])
def delete_password():

    user_hash = session.get('user_hash')

    origin_url = request.json.get('origin_url')
    origin_name = request.json.get('origin_name')
    origin_password = request.json.get('origin_password')
    password_id = request.json.get('password_id')

    backend_functions.delete_password(user_hash, origin_url, origin_name, origin_password, password_id)

    passwords = backend_functions.fetch_passwords(user_hash)
    session['passwords'] = passwords

    return jsonify(success=True)


@app.route('/forgot_my_password', methods=['GET', 'POST'])
def forgot_my_password():

    if request.method == 'POST':

        pass

    elif request.method == 'GET':

        return render_template('recuperacaoConta.html')


@app.route('/logout')
def logout():

    # Clear the session data
    session.clear()
    # Redirect the user to the home page or any other desired location
    return redirect('/')


if __name__ == '__main__':
    app.run()