from dotenv import load_dotenv
from colorama import Fore
import os
import pymysql


# ---------------------------- #

load_dotenv()       # import file from .env


# read variable
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# ---------------------------- #

# print coloring

def print_color(string: str, mode: str="r"):

    if mode == "r":
        print(Fore.RED + f"\n{string}\n" + Fore.RESET)
    
    elif mode == "g":
        print(Fore.GREEN + f"\n{string}\n" + Fore.RESET)
    
    elif mode == "b":
        print(Fore.BLUE + f"\n{string}\n" + Fore.RESET)
    
    elif mode == "c":
        print(Fore.CYAN + f"\n{string}\n" + Fore.RESET)
    
    elif mode == "y":
        print(Fore.YELLOW + f"\n{string}\n" + Fore.RESET)
    
    elif mode == "m":
        print(Fore.MAGENTA + f"\n{string}\n" + Fore.RESET)

    else:
        print(f"\n{string}\n")

# ---------------------------- #