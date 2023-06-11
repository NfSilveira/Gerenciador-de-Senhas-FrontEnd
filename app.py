from flask import Flask, render_template, request, redirect
import backend.backend_functions as backend_functions
import os

app = Flask(__name__, template_folder='frontend/html', static_folder='static')
secret_key = os.urandom(12).hex()
app.secret_key = secret_key
app.debug = True

@app.route('/')
def index():
    
    return render_template('telaInicial.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        # Get the user's input from the registration form
        username = request.form.get('email', '')
        password = request.form.get('password', '')

        # Hash the password
        hashed_password = backend_functions.hash_password(password)

        # Save the username and hashed password in the database
        backend_functions.save_to_database(username, hashed_password)

        # Redirect to the home page
        return redirect('/')
    
    elif request.method == 'GET':

        return render_template('cadastro.html')


@app.route('/login')
def login():

    return render_template('login.html')


if __name__ == '__main__':
    app.run()