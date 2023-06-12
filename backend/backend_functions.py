import bcrypt
import psycopg2


def hash_password(password):

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')


def connect():

    try:

        connection = psycopg2.connect(
            host = "127.0.0.1",
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
    cur.close()

    if result is not None:

        user_name = result[0].split(' ')[0] if result[0] is not None and result[0] != '' else 'Usuário'

        hashed_password = result[1].encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):

            return True, user_name
        
        else:

            return False, None