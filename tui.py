import keyboard as K
import getpass
import time
import sys
import os
import blockchain as BC
import colorama
import getch
import random

# colorama.just_fix_windows_console()

__IS_LOGGED_IN = False
__IS_MINING = False

def pprint(*args, sep=" ", end="\n", speed=0.0001):
    for i in args:
        j = str(i)
        for k in j:
            print(k, end="")
            time.sleep(speed)
            sys.stdout.flush()
            sys.stdout.buffer.flush()
        print(end=sep)

    print(end=end)

def clear():
    for i in range(120):
        print("       "*80)
    
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except:
        try:
            os.system("clear")
        except:
            try:
                os.system("cls")
            except: print(chr(27) + "[2J")

def normal_input(prompt: str):
    pass

def secret_input(prompt: str):
    print(prompt, end="")
    passw = getpass.getpass(prompt)
    print("\033[F", end="")
    print(prompt, end="", flush=True)
    print("*" * (len(passw) if len(passw) < 60 else 16), end="")
    print()
    return passw


############################################################
############################################################
############################################################

def main_menu():
    clear()
    kbit = getch.KBHit()
    t1 = time.time()
    a = "◜◟◡◞◝◠oo"
    l = 0
    while True:
        t2 = time.time()
        c = a[l % len(a)]
        if l > len(a):
            l = 0
        
        if t2 - t1 >= 0.1:
            l += 1
            t1 = t2
        
        statuses = BC.get_statuses()
        status = [
            "╭―Statuses―[" + str(c) + "]―――――――――――――――――――――――――――――",
            "│   Current User            : " + str(statuses[0]),
            "│   Status                  : " + str(statuses[1]),
            "│   Last Block              : " + str(statuses[2]),
            "│   Current Challange Block : " + str(statuses[3]),
        ]

        menu = [
            "├―Main Menu――――――――――――――――――――――――――――――――",
            "│  ( 1 ) Register User",
            "│  ( 2 ) Change User Password",
            "│  ( 3 ) Generate Gift Card",
            "│  ( 4 ) Use Gift Card",
            "│  ( 5 ) Export Gift Card Data",
            "│  ( 9 ) Login" if not __IS_LOGGED_IN else "|  (0). Logout",
            "│  (ESC) Exit",
            "╰―――――――――――――――――――――――――――――――――――――――――"
        ]

        sys.stdout.buffer.write(bytes("\033[F"*(len(status) + len(menu)), "utf-8"))
        sys.stdout.buffer.write(bytes("\n".join(status + menu), 'utf-8'))
        sys.stdout.buffer.write(bytes("\n", 'utf-8'))
        sys.stdout.buffer.flush()

        if kbit.kbhit():
            command = kbit.getch()
            print(command)
            if   command =="1":
                register_user()
            elif command == "2":
                change_user_password()
            elif command == "3":
                generate_gift_card()
            elif command == "4":
                use_gift_card()
            elif command == "5":
                export_gift_card()
            elif command == "9":
                login()
            elif ord(command) == 27:
                exit_menu()
            else:
                pprint("Invalid Input, Try Again                │", end="")
                print(" "*80)
                time.sleep(2)
                sys.stdout.buffer.write(bytes("\033[F", "utf-8"))
                print("│                                        ")
                clear()

def register_user():
    while True:
        clear()
        print("╭―User Registration――――――――――――――――――――")
        print("│ New Username     :")
        print("│ Confirm Username :")
        print("│ New Password     :")
        print("│ Confirm Password :")
        print("╰――――――――――――――――――――――――――――――――――――――")
        sys.stdout.buffer.write(bytes("\033[F", "utf-8"))
        sys.stdout.buffer.write(bytes("\033[F", "utf-8"))
        sys.stdout.buffer.write(bytes("\033[F", "utf-8"))
        sys.stdout.buffer.write(bytes("\033[F", "utf-8"))
        sys.stdout.buffer.write(bytes("\033[F", "utf-8"))
        username_1 = input("│ New Username     : ")
        if username_1 == None or username_1 == "":
            print("\n"*3)
            pprint("  Username Cannot Be Empty")
            time.sleep(1)
            clear()
            continue
        
        if len(username_1) < 6:
            print("\n"*3)
            pprint("  Username must be over 6 character long")
            time.sleep(1)
            clear()
            continue

        username_2 = input("│ Confirm Username : ")
        if username_1 != username_2:
            print("\n"*2)
            pprint("  Please Re-confirm your Username!")
            time.sleep(1)
            clear()
            continue

        password_1 = secret_input("│ New Password     : ")
        if password_1 == None or password_1 == "":
            print("\n"*2)
            pprint("  Password Cannot Be Empty")
            time.sleep(1)
            clear()
            continue
        
        if len(password_1) < 6:
            print("\n"*2)
            pprint("  Password Cannot Be Less Than 6 character")
            time.sleep(1)
            clear()
            continue

        password_2 = secret_input("│ Confirm Password : ")
        if password_1 != password_2:
            print("╰――――――――――――――――――――――――――――――――――――――\n")
            pprint("Please Re-confirm your Password!")
            time.sleep(1)
            clear()
            continue
        else:
            print("╰――――――――――――――――――――――――――――――――――――――\n")
            break

    a = "-/|\\"
    for i in range(40):
        print("  Registering User... " + a[i % len(a)], end="\r")
        time.sleep(random.randint(100, 500) / 10000)
    print(username_1)
    print(password_1)
    clear()

def change_user_password():
    while True:
        clear()
        print("╭―User Password Change ― Login――――――――――――")
        print("│ Username          :")
        print("│ Existing Password :")
        print("│ New Password      :")
        print("│ Confirm Password  :")
        print("╰―――――――――――――――――――――――――――――――――――――――――")
        sys.stdout.buffer.write(bytes("\033[F", "utf-8"))
        sys.stdout.buffer.write(bytes("\033[F", "utf-8"))
        sys.stdout.buffer.write(bytes("\033[F", "utf-8"))
        sys.stdout.buffer.write(bytes("\033[F", "utf-8"))
        sys.stdout.buffer.write(bytes("\033[F", "utf-8"))
        username_1 = input("│ Username          : ")
        if username_1 == None or username_1 == "":
            print("\n"*3)
            pprint("  Username Cannot Be Empty")
            time.sleep(1)
            clear()
            continue
        
        if len(username_1) < 6:
            print("\n"*3)
            pprint("  Username must be over 8 character long")
            time.sleep(1)
            clear()
            continue
        
        password_confirm = secret_input("│ Existing Password : ")
        if password_confirm == None or password_confirm == "":
            print("\n"*2)
            pprint("  Password Cannot Be Empty")
            time.sleep(1)
            clear()
            continue
        
        password_1 = secret_input("│ New Password      : ")
        if password_1 == None or password_1 == "":
            print("\n"*2)
            pprint("  Password Cannot Be Empty")
            time.sleep(1)
            clear()
            continue
        
        if len(password_1) < 6:
            print("\n"*2)
            pprint("  Password Cannot Be Less Than 6 character")
            time.sleep(1)
            clear()
            continue

        password_2 = secret_input("│ Confirm Password  : ")
        if password_1 != password_2:
            print("╰――――――――――――――――――――――――――――――――――――――\n")
            pprint("Please Re-confirm your Password!")
            time.sleep(1)
            clear()
            continue
        else:
            print("╰――――――――――――――――――――――――――――――――――――――\n")
            break
        
        

def generate_gift_card():
    clear()
    pass

def use_gift_card():
    clear()
    pass

def export_gift_card():
    clear()
    pass
    
def login():
    clear()
    time.sleep(0.5)
    pprint("User Login")
    pprint("| Username :", end="")
    username = input()
    time.sleep(0.1)
    password = secret_input("| Password : ")
    pprint("+--------")


    pprint(username, password)
    clear()

def exit_menu():
    pprint("_Good Bye!")
    time.sleep(1)
    exit(0)


main_menu()