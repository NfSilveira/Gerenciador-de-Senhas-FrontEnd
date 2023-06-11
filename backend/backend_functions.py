import bcrypt
import psycopg2


def hash_password(password):

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')


def connect():

    try:

        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(
            host = "127.0.0.1",
            database = "passwizard",
            user = "passmaster",
            password = "@2023_ComputerMagic",
            port = 5432
        )

        print("Connection established!")

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