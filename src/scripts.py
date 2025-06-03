from packages import *

# ------------------------------------------------------ #

class MySql:

    def __init__(self):

        try:
            self.connection = pymysql.connect(host= DB_HOST, user= DB_USER, passwd= DB_PASSWORD, database= DB_NAME)

        except Exception as E:

            print_color(f"An error to connect to data base. '{E}'.")

# ------------------------ #

    def get_cursor(self):
        return self.connection.cursor()

# ------------------------ #
    
    def creat_record(self, query, paramas):
        
        cursor = self.get_cursor()

        cursor.execute(query, paramas)

        self.connection.commit()

        cursor.close()

# ------------------------ #

    def select(self, query, paramas):
        
        cursor = self.get_cursor()

        cursor.execute(query, paramas)

        retsult = cursor.fetchall()

        cursor.close()

        return retsult

# ------------------------ #

    def update_record(self, query, paramas):
        
        cursor = self.get_cursor()

        cursor.execute(query, paramas)

        self.connection.commit()

        cursor.close()

# ------------------------ #

    def delete(self, query, params):
        
        cursor = self.get_cursor()

        cursor.execute(query, params)

        self.connection.commit()

        cursor.close()

# ------------------------ #

    def close(self):

        self.connection.close()

# ------------------------ #

# ------------------------------------------------------ #

class ConnectToDB:

    def __init__(self, query, *args):
        
        self.query = query
        self.paramas = args if args else ()
        self.db = MySql()
        self.close = self.db.close

# ------------------------ #
    
    def select_choosen(self):

        result = self.db.select(self.query, self.paramas)

        self.close()

        return result[0] if result else None
    
# ------------------------ #
    
    def select_all(self):

        result = self.db.select(self.query, self.paramas)

        self.close()

        return result
    
# ------------------------ #

    def insert(self):

        self.db.creat_record(self.query, self.paramas)

        self.close()

# ------------------------ #

    def update(self):

        self.db.update_record(self.query, self.paramas)

        self.close()

# ------------------------ #

    def delete(self):

        self.db.delete(self.query, self.paramas)

        self.close()

# ------------------------ #

# ------------------------------------------------------ #

class Orders:
    pass

# ------------------------------------------------------ #

class Product:
    def __init__(self, product_id):
        self.product_id = product_id

        product_info = self.product_data()

        self.category_id = product_info[1]
        self.brand = product_info[2]
        self.model = product_info[3]
        self.quantity = product_info[4]
        self.buy_price = product_info[5]
        self.sell_price = product_info[6]

# ------------------------ #
    
    def product_data(self):

        query = "select * from products where ProductID = %s"

        params = (self.product_id, )

        result = ConnectToDB(query, *params).select_choosen()

        return result

# ------------------------ #

    @staticmethod
    def add_new_product():
        pass

# ------------------------ #

# ------------------------------------------------------ #

class Category:

    def __init__(self, category_id):
        self.category_id = category_id

        category_info = self.category_data()

        self.category_name = category_info[1]
        self.category_description = category_info[2]
        self.category_parent = category_info[3]

# ------------------------ #

    def category_data(self):

        query = "select * from productcategory where CategoryID = %s"

        params = (self.category_id, )

        result = ConnectToDB(query, *params).select_choosen()

        return result

# ------------------------ #

    @staticmethod
    def all_category_data():

        query = "select * from productcategory"

        result = ConnectToDB(query).select_all()

        return result

# ------------------------ #

    @staticmethod
    def show_all_category():
        
        data = Category.all_category_data()

        for index, info in enumerate(data, start= 1):

            print_color(f"{index}. category id: {info[0]} --- category name: {info[1]} --- description: '{info[2]}' --- category parent: {info[3]}", "m")

            print_color("-" * 40, "b")
            
# ------------------------ #

    @staticmethod
    def add_new_category():
        pass

# ------------------------ #

# ------------------------------------------------------ #

class User:
    
    def __init__(self, username):
        self.username = username

        user_info = self.user_data()

        self.userid = user_info[0]
        self.password = user_info[2]
        self.name = user_info[3]
        self.email = user_info[4]
        self.permision = user_info[5]
        self.balance = user_info[6]
# ------------------------ #

    def user_data(self):
        
        query = "select * from users where username = %s"

        user = ConnectToDB(query, self.username)

        result = user.select_choosen()

        return result       

# ------------------------ #

    def current_balance(self):

        user_data = self.user_data()

        print_color(f"Your current balance is '{user_data[6]}'$.", "g")

        return user_data[6]

# ------------------------ #

    def update_balance(self, amount: int, mode: str="buy"):

        admin = User("mhghasri")

        if mode == "buy":
            self.balance -= amount

            admin.balance += amount

        elif mode == "refund":

            self.balance += amount

            admin.balance -= amount

        elif mode == "charge":

            self.balance += amount

        elif mode == "admin_buy":

            admin.balance -= amount

        else:
            raise ValueError("Invalid input for mode in User.update_balance.")

        query = "update users set Balance = %s where UserName = %s"

        params = (self.balance, self.username)

        ConnectToDB(query, *params).update()

        if mode in ("buy", "refund", "admin_buy"):

            admin_query = "update users set Balance =%s where UserName = %s"

            admin_params = (admin.balance, admin.username)

            ConnectToDB(admin_query, *admin_params).update()       

        print_color(f"Your transaction is successfully compelete. Your current balance: '{self.balance}'$.", "g")  

# ------------------------ #

    @classmethod
    def login(cls):
        username_list = User.all_username_list()

        while True:

            username = input("\nPlease enter your user name: ")

            if username not in username_list:
                print_color("invalid username.")

            else:
                
                user = cls(username)

                user_information = user.user_data()

                break

        for time_remaining in range(3, 0, -1):

            password = input("\nPlease enter your password: ")

            if password == user_information[2]:

                print_color("login successfully.", "g")

                return cls(username)
            
            elif time_remaining == 1:
                print_color("Out of chance. Please try again later.")

                return False
            
            else:
                print_color(f"invalid password. Please try again. reamainig chance: {time_remaining - 1}.")

# ------------------------ #

    @classmethod
    def user_data_by_id(cls, userid):

        query = "select * from users where userid = %s"

        params = (userid)

        user = ConnectToDB(query, params)

        result = user.select_choosen()

        return cls(result[1])

# ------------------------ #

    @staticmethod
    def signup():
        usernames_list = User.all_username_list()

        while True:

            username = input("\nPlease enter your user name: ")

            if username in usernames_list:

                print_color("This username is already exist. please enter diferent username.")

            else:
                break

        for time_remain in range(3, 0, -1):

            password = input("\nPlease enter your password: ")

            if User.password_validation(password):
                break

            elif time_remain == 1:

                print_color("Out of chance. Please try again later.")

                return None

            else:
                print_color(f"Please be pation. time remainig: {time_remain - 1}.")

        fname = input("\nPlease enter your first name: ")

        lname = input("\nPlease enter your last name: ")

        email = input("\nPlease enter your email: ")

        name = f"{fname} {lname}"
        
        query = "insert into users (UserName, password, Name, Email) values (%s, %s, %s, %s)"

        params = (username, password, name, email)

        creat_user = ConnectToDB(query, *params)

        creat_user.insert()

        print_color(f"signup successfully. username: {username} --- password: {password}.", "g")

# ------------------------ #

    @staticmethod
    def password_validation(password: str):
        lower = upper = digit = other = 0

        if len(password) in range(8, 33):

            for ch in password:
                if ch.islower():
                    lower += 1

                elif ch.isupper():
                    upper += 1

                elif ch.isdigit():
                    digit += 1

                else:
                    other += 1

            if (lower > 0) and (upper > 0) and (digit > 0) and (other > 0):
                return True
            
            else:
                print_color("Your password need at least 1 upper - lower - digit - other case(s).")
                return False

        else:

            print_color("Your password must be 8 - 32 char.")

            return False

# ------------------------ #

    @staticmethod
    def all_username_list():

        query = "select username from users"

        result = ConnectToDB(query).select_all()

        username_tuple = tuple(username[0] for username in result)

        return username_tuple

# ------------------------ #



# ------------------------ #

# ------------------------------------------------------ #

class Admin(User):
    pass

# ------------------------------------------------------ #


# mh = User.user_data_by_id(1)

# mh = User.login()
# print(mh.userid)
# print(mh.username)
# print(mh.password)
# print(mh.name)
# print(mh.email)
# print(mh.permision)
# print(mh.balance)

# print(User.all_username_list())

# ali = User("alinorouzi")

# ali.current_balance()

Category.show_all_category()