import sqlite3
import getpass

def create_user_table():
    """
    Simple function to create a database table
    CREATE tale if it doesn't exist, username and password should be text
    """
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username text, password text)''')
    conn.commit()
    conn.close()

def register_user(username, password):
    """
    Simple function to insert a user into the database upon registering
    """
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()
    print("Successfully registered user:", username)
    conn.close()

def login_user(username, password):
    """
    Simple function to check if a user is registered
    If registered returns True else returns False
    -> Gets everything from users table where ? is a placeholder for the
       respective username and password
    """
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return True
    else:
        return False


def authenticate():
    # I created the main function from which all of our code should integrate
    # Hence the while loop, allowing one to use the Code Clinics program after having logged in.
    # Within the while loop, after one logs in, functionality of calendar view, volunteering, etc. 
    # - Should be added bumokat022@student.wethinkcode.co.za Nukegen98
    create_user_table()
    print("-------------------- Code Clinics Scheduler (v 1.0.1) --------------------")
    while True:
        print("-------------------- Enter (1) to register, (2) to login, (3) to exit --------------------")
        choice = int(input().strip())
        if choice == 1:
            username = input("Enter a username: ").strip()
            password = getpass.getpass("Enter a password: ").strip()
            register_user(username, password)
        elif choice == 2:
            username = input("Enter your username: ").strip()
            password = getpass.getpass("Enter your password: ").strip()
            if login_user(username, password):
                print("Successful login")
                return username, password
                # Busi and Conert you are to call your functions here to call the api so
                # that the logged in user can have multiple options. 
                # These options include - booking, canceling and volunteering
            else:
                print("-------------------- Incorrect username or password --------------------")
        elif choice == 3:
            return '', ''
        else:
            print("Invalid choice, try again")

if __name__ == '__main__':
    user_name, password = authenticate()
