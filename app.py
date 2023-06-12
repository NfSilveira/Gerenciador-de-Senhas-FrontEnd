from flask import Flask, jsonify, render_template, request, session, redirect
import backend.backend_functions as backend_functions
import os
import re

app = Flask(__name__, template_folder='frontend/html', static_folder='static')
secret_key = os.urandom(12).hex()
app.secret_key = secret_key

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
        return redirect('/'), jsonify({'message': 'Registration successful', 'type': 'success'})
    
    elif request.method == 'GET':

        return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('Email')

        if request.form.get('Password') != '' and email != '':

            match, username = backend_functions.check_login_credentials(email, request.form.get('Password'))

            if match:

                session['username'] = username
                return redirect('/dashboard')
            
            else:
                
                return redirect('/')

    elif request.method == 'GET':

        return render_template('login.html')
    

@app.route('/dashboard')
def dashboard():

    return render_template('senhasCadastradas.html')


if __name__ == '__main__':
    app.run()