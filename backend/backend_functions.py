import bcrypt
import psycopg2
import base64
from cryptography.fernet import Fernet

encryption_key = b'UfGTypNgJzQ6ooSFkLVRpkbv0nLrqLwY'
encoded_key = base64.urlsafe_b64encode(encryption_key)

# Initialize the Fernet cipher object with the encoded key
cipher = Fernet(encoded_key)


def hash_password(password):

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')


def connect():

    try:

        connection = psycopg2.connect(
            host = "20.226.60.21",
            database = "passwizard",
            user = "passmaster",
            password = "@2023_ComputerMagic",
            port = 5432
        )

        return connection

    except (Exception, psycopg2.DatabaseError) as e:

        print(str(e))


def save_to_database(full_name, phone_number, email, password):

    try:

        conn = connect()

        cur = conn.cursor()


        cur.execute(f"INSERT INTO login_credentials (_full_name, _phone_number, _user_email, _user_password) VALUES ('{full_name}', '{phone_number}', '{email}', '{password}');")

        conn.commit()
        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as e:

        print(str(e))


def check_login_credentials(email, password):

    conn = connect()

    cur = conn.cursor()
    cur.execute(f"SELECT _full_name, _user_password FROM login_credentials WHERE _user_email = '{email}';")
    result = cur.fetchone()

    if result is not None:

        user_name = result[0].split(' ')[0] if result[0] is not None and result[0] != '' else 'Usuário'

        hashed_password = result[1].encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):

            cur.execute(f"SELECT _user_hash FROM login_credentials WHERE _user_email = '{email}' AND _user_password = '{result[1]}';")
            user_hash = cur.fetchone()[0]
            cur.close()

            return True, user_name, user_hash
        
        else:

            return False, None
        

def fetch_passwords(user_hash):

    conn = connect()

    cur = conn.cursor()
    cur.execute(f"SELECT _origin, _origin_username, _origin_password FROM stored_passwords WHERE _user_hash = '{user_hash}';")
    passwords = cur.fetchall()

    if passwords:

        decoded_passwords_list = []

        for password in passwords:
            password_list = list(password)

            encoded_password = password_list[2].encode()
            decoded_password = cipher.decrypt(base64.b64decode(encoded_password)).decode()
            password_list[2] = decoded_password
            decoded_password = tuple(password_list)

            decoded_passwords_list.append(decoded_password)

    return decoded_passwords_list or []


def add_new_password(user_hash, origin_url, origin_name, origin_password):

    encoded_password = base64.b64encode(cipher.encrypt(origin_password.encode())).decode()

    conn = connect()

    cur = conn.cursor()
    query = "INSERT INTO stored_passwords(_user_hash, _origin, _origin_username, _origin_password) VALUES (%s, %s, %s, %s);"
    cur.execute(query, (user_hash, origin_url, origin_name, encoded_password))

    conn.commit()

    cur.close()
    conn.close()