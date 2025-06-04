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

class ShipingCart:
    
    def __init__(self):
        pass
# ------------------------ #

    def 

# ------------------------ #

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
    def all_product_data():

        query = "select * from products"

        result = ConnectToDB(query).select_all()

        return result

# ------------------------ #

    @staticmethod
    def show_all_product():
        
        product_data = Product.all_product_data()

        product_id_list = []

        for index, info in enumerate(product_data, start=1):

            print_color(f"{index}. Product ID: {info[0]} --- Brand: {info[2]} --- model: {info[3]} --- quantity: {info[4]} --- price: '{info[6]}'$.", "m")

            category = Category(info[1])

            if not category.category_parent:
                print_color(f"category: {category.category_name}.", "m")

            else:
                parent = Category(category.category_parent)

                print_color(f"category: {category.category_name} ---> {parent.category_name}", "m")

            print_color("-" * 40, "b")

            product_id_list.append(info[0])

        return product_id_list          # use it for edit product

# ------------------------ #

    @staticmethod
    def add_new_product():

        print_color("These are all categorys.", "y")
        
        category = Category.show_all_category()

        admin = Admin("mhghasri")

        while True:

            category_id = input("\nPlease enter category id for add new product: ")

            try:

                if int(category_id) in category:

                    category_id = int(category_id)

                    category_object = Category(category_id)

                    parent_object = Category(category_object.category_parent)

                    if  not category_object.category_parent:

                        print_color(f"category name: {category_object.category_name}", "y")


                    else:

                        print_color(f"category name: {category_object.category_name} ---> {parent_object.category_name}.", "y")

                    while True:

                        are_you_sure = input("\nAre you sure? (yes, no): ")

                        if are_you_sure in ("yes", "y"):
                            break

                        elif are_you_sure in ("no", "n"):
                            print_color("Transaction cancelled.")
                            return None
                        
                        else:
                            print_color("yes or no is accepted.")
                            
                    break

                else:

                    print_color("Invalid input please focus a bit more.")

            except ValueError:
                print_color("Please enter vaild number.")



        brand = input("\nEnter brand of new product: ")

        model = input("\nEnter model of new product: ")

        while True:
            quantity = input("\nEnter quantity of product: ")
            buy_price = input("\nEnter buying price of product: ")

            try:
                quantity = int(quantity)
                buy_price = float(buy_price)

            except ValueError:
                print_color("invalid input for quanty or buying price. Please enter valid number.")

            else:
                break

        sell_price = 1.3 * buy_price

        amount = quantity * buy_price

        if amount > admin.balance:

            print_color(f"You dont have enough balance. current balance: '{admin.balance}'$. product amount: '{amount}'$.")

            quantity = admin.balance // buy_price

            print_color(f"buy you cant buy: {quantity}.", "y")

            while True:

                yes_or_no = input("\nDo you want this? (yes, no): ")

                if yes_or_no in ("yes", "y"):

                    amount = quantity * buy_price
                    break

                elif yes_or_no in ("no", "n"):
                    print_color("Transaction cancelled.")
                    return None
                            
                else:
                    print_color("Just yes or no is accepted.")

        admin.update_balance(amount, "admin_buy")

        query = "insert into products (categoryID, brand, model, quantity, buyprice, sellprice) values (%s, %s, %s, %s, %s, %s)"

        params = (category_id, brand, model, quantity, buy_price, sell_price)

        ConnectToDB(query, *params).insert()

        print_color("New product successfully aded to product.", "g")
        

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

        category_id_list = []

        for index, info in enumerate(data, start= 1):

            print_color(f"{index}. category id: {info[0]} --- category name: {info[1]} --- category parent: {info[3]}", "m")

            print(f"description: {convert(info[2])}")

            print_color("-" * 40, "b")

            category_id_list.append(info[0])

        return category_id_list
            
# ------------------------ #

    @staticmethod
    def add_new_category():

        print_color("This is all category: ", "y")

        category_data = Category.show_all_category()

        name = input("\nPlease enter category name: ")

        description = input("\nPlease enter description: ")

        while True:

            parent_id = input("\nIf your category has parent please enter id of that (iPhone -> smart phone): ")

            if parent_id == "":
                parent_id = None
                break

            elif not parent_id.isdigit():
                print_color("Parent id must be a int number.")
                continue

            parent_id = int(parent_id)

            if parent_id not in category_data:
                print_color("Please enter valid parent id.")

            else:
                break

        query = "insert into productcategory (categoryname, description, parentID) values (%s, %s, %s)"

        params = (name, description, parent_id)

        ConnectToDB(query, *params).insert()

        print_color("New category add successfully.", "g")

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

        print_color(f"Your transaction is successfully compelete.", "g")  

        balance = self.current_balance()       

# ------------------------ #

    def buy_product(self):

        print_color("Here you are these are all product:", "c")

        product_data = Product.show_all_product()

        while True:

            try: 

                product_id = input("\nPlease enter product id you want to buy: ")

                product_obj = Product(int(product_id))

                category_obj = Category(product_obj.category_id)

            except (ValueError, TypeError):
                
                print_color("Invalid input. Please enter currect input.")

            else:
                
                print_color("-" * 40, "b")

                break
        
        if not category_obj.category_parent:
                print_color(f"category: {category_obj.category_name}.", "m")

        else:
            parent = Category(category_obj.category_parent)

            print_color(f"category: {category_obj.category_name} ---> {parent.category_name}", "m")

        print_color(f"product Id: {product_obj.product_id} --- brand: {product_obj.brand} --- model: {product_obj.model} --- quantity: {product_obj.quantity} --- price: '{product_obj.sell_price}'$.", "c")

        while True:

            yes_or_no = input("\nAre your sure to buy it? (yes, no): ")

            if yes_or_no in ("yes", "no"):

                break

            else:
                print_color("Just yes/no accepted. Please try again.")

        if yes_or_no == "no":
            print_color("Tranaction successfully canceled.", "g")
            return None
        

        while True:

            try:
                quantity = int(input("\nPlease enter quantity you want: "))

            except:
                print_color("Please enter valid number. try again.")

            else:
                
                if product_obj.quantity < quantity:

                    print_color("not enough quantity. Please try again.")

                else:

                    break

        amount = quantity * product_obj.sell_price

        if amount > self.balance:

            print_color(f"Not enough money. current balance: '{self.balance}'$. amount: {amount}.")

            quantity = self.balance // product_obj.sell_price

            print_color(f"But you can buy {quantity} of this product.", "g")

            while True:
                yes_or_no = input("\nAre your sure to buy it? (yes, no): ")

                if yes_or_no in ("yes", "no"):

                    break

                else:
                    print_color("Just yes/no accepted. Please try again.")

            if yes_or_no == "no":
                print_color("Tranaction successfully canceled.", "g")

                return None

            else:
                amount = quantity * product_obj.sell_price

        self.update_balance(amount)




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
    
    def __init__(self, username):
        super().__init__(username)

    def add_new_category(self):
        Category.add_new_category()

    def show_all_category(self):
        Category.show_all_category()

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

ali = User("alinorouzi")

# ali.current_balance()

# Category.add_new_category()

# Category.show_all_category()

# Product.show_all_product()

ali.buy_product()
