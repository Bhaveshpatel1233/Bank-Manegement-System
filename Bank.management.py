# BANK MANAGEMENT SYSTEM WITH MYSQL

import mysql.connector

# 1. DATABASE CONNECTION

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bhavesh123",
        database="bank_manegement_system"
    )

    cursor = conn.cursor()

    if conn.is_connected():
        print("Connected to MySQL Database Successfully!")

except mysql.connector.Error as err:
    print("Database Connection Error:", err)
    exit()


# 2. CUSTOM EXCEPTIONS

class LoginError(Exception):
    pass


class InsufficientBalance(Exception):
    pass


# 3. REGISTRATION FUNCTION

def registration():

    print("\n===== USER REGISTRATION =====")

    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    address = input("Enter your address: ")
    phoneno = input("Enter your phone number: ")
    userid = input("Enter your username: ")
    password = input("Enter your password: ")
    confirmpassword = input("Confirm your password: ")

    if password != confirmpassword:
        print("Password and Confirm Password do not match!")
        return

    try:

        query = """
        INSERT INTO bank_system
        (name, age, address, phoneno, userid, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            name,
            age,
            address,
            phoneno,
            userid,
            password
        )

        cursor.execute(query, values)

        conn.commit()

        print("\nRegistration Successful!")

    except mysql.connector.IntegrityError:
        print("Username already exists!")

    except mysql.connector.Error as err:
        conn.rollback()
        print("Registration Error:", err)


# 4. LOGIN FUNCTION

def login(userid, password):

    try:

        query = """
        SELECT userid
        FROM bank_system
        WHERE userid = %s AND password = %s
        """

        cursor.execute(query, (userid, password))

        user = cursor.fetchone()

        if user:
            print("\nLogin Successful!")
            return True

        else:
            raise LoginError("Invalid Username or Password!")

    except LoginError as e:
        print(e)
        return False


# 5. DEPOSIT FUNCTION

def deposit(userid):

    try:

        amount = int(input("Enter deposit amount: "))

        if amount <= 0:
            print("Please enter a valid amount!")
            return

        query = """
        UPDATE bank_system
        SET deposit = deposit + %s,
            show_balance = show_balance + %s
        WHERE userid = %s
        """

        cursor.execute(query, (amount, amount, userid))

        conn.commit()

        print(amount, "Deposited Successfully!")

    except ValueError:
        print("Please enter numbers only!")

    except mysql.connector.Error as err:
        conn.rollback()
        print("Deposit Error:", err)


# 6. WITHDRAWAL FUNCTION

def withdrawal(userid):

    try:

        amount = int(input("Enter withdrawal amount: "))

        if amount <= 0:
            print("Please enter a valid amount!")
            return

        query = """
        SELECT show_balance
        FROM bank_system
        WHERE userid = %s
        """

        cursor.execute(query, (userid,))

        result = cursor.fetchone()

        if result is None:
            print("User not found!")
            return

        current_balance = result[0]

        if amount > current_balance:

            raise InsufficientBalance("Insufficient Balance!")

        else:

            query = """
            UPDATE bank_system
            SET withdraw = withdraw + %s,
                show_balance = show_balance - %s
            WHERE userid = %s
            """

            cursor.execute(query, (amount, amount, userid))

            conn.commit()

            print(amount, "Withdrawn Successfully!")

    except ValueError:
        print("Please enter numbers only!")

    except InsufficientBalance as e:
        print(e)

    except mysql.connector.Error as err:
        conn.rollback()
        print("Withdrawal Error:", err)


# 7. SHOW BALANCE FUNCTION

def show_balance(userid):

    try:

        query = """
        SELECT show_balance
        FROM bank_system
        WHERE userid = %s
        """

        cursor.execute(query, (userid,))

        result = cursor.fetchone()

        if result:
            print("\nYour Account Balance:", result[0])

        else:
            print("Account not found!")

    except mysql.connector.Error as err:
        print("Balance Error:", err)


# 8. ACCOUNT MENU

def account_menu(userid):

    while True:

        print("\n===== YOUR ACCOUNT MENU =====")

        print("1. Deposit")
        print("2. Withdraw")
        print("3. Show Balance")
        print("4. Exit")

        try:

            choice = int(input("Enter your choice: "))

            if choice == 1:

                deposit(userid)

            elif choice == 2:

                withdrawal(userid)

            elif choice == 3:

                show_balance(userid)

            elif choice == 4:

                print("Thank you for visiting!")

                break

            else:

                print("Invalid Choice! Try Again.")

        except ValueError:
            print("Please enter numbers only!")


# 9. MAIN MENU

try:

    while True:

        print("\n===== WELCOME TO BANK MANAGEMENT SYSTEM =====")

        print("1. Registration")
        print("2. Login")
        print("3. Exit")

        try:

            choice = int(input("Please enter your choice: "))

            if choice == 1:

                registration()

            elif choice == 2:

                print("\n===== USER LOGIN =====")

                userid = input("Enter username: ")

                password = input("Enter password: ")

                result = login(userid, password)

                if result:

                    account_menu(userid)

            elif choice == 3:

                print("Thank you for using our Bank Management System!")

                break

            else:

                print("Invalid Choice! Please try again.")

        except ValueError:
            print("Please enter numbers only!")


finally:

    # 10. CLOSE DATABASE CONNECTION

    if conn.is_connected():

        cursor.close()

        conn.close()

        print("\nDatabase Connection Closed!")


