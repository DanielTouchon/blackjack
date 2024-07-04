from hashlib import sha256
import csv
from time import sleep

cls = lambda: print("\033c\033[3J", end='')

def login(name="",pw=""):
    with open("users.csv", mode="r", encoding='utf-8') as file:
        reader = csv.reader(file)
        if name=="" and pw=="":
            name = input("Your registered name? ")
            pw = input("Your passphrase? ")
        for [reg_name, reg_pass] in reader:
            name_hash = sha256(name.encode('utf-8')).hexdigest()
            pw_hash = sha256(pw.encode('utf-8')).hexdigest()
            if name_hash != reg_name or pw_hash != reg_pass:
                check = False
            else:
                check = True
                break
    return check,name,pw

def register(new_name, new_pw):
    new_name_hash = sha256(new_name.encode('utf-8')).hexdigest() 
    new_pw_hash = sha256(new_pw.encode('utf-8')).hexdigest()

    with open("users.csv", mode="a", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([new_name_hash, new_pw_hash])

def login_loop():
    LoggedIn = False
    while not LoggedIn:
        check,name,pw = login()
        if check:
            print(f"Hey {name.capitalize()}. Welcome back.")
            LoggedIn = True
            break
        else:
            print("Account not found.")
            choice = input("Do you want to register? (y/n) ")
            while choice:
                cls()
                conf_pw = input("Confirm your passphrase: ")
                if pw == conf_pw:
                    register(name,pw)
                    login(name,pw)
                    LoggedIn = True
                    print(f"Welcome, {name.capitalize()}!")
                    break
                else:
                    print("The passphrases don't match.")
                    sleep(2)
            break