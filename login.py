import hashlib

from rsa_crypto import keys
import pickle

invalidNames = ["All"]

def login(acc=None):
    try:
        pickle.load(open("Accounts\Accs.p", "rb"))
    except:
        pickle.dump({}, open("Accounts\Accs.p", "wb"))
    try:
        pickle.load(open("Accounts\Keys\public.p", "rb"))
    except:
        pickle.dump({}, open("Accounts\Keys\public.p", "wb"))
    try:
        pickle.load(open("Accounts\Keys\private.p", "rb"))
    except:
        pickle.dump({}, open("Accounts\Keys\private.p", "wb"))

    if not(acc):
        welcome = input("Do you have an acount? y/n: ")
        if welcome == "n":
            while True:
                username  = input("\nEnter a username: ")
                password  = input("Enter a password: ")
                password1 = input("Confirm password: ")

                try:
                    if not(username in invalidNames or ", " in username):
                        accs = pickle.load(open("Accounts\Accs.p", "rb"))
                        accs[username]
                    
                        print("Account already exists\n")
                    else: print("Username is invalid")
                    return login()

                except:
                    if password == password1:
                        public, private = keys()

                        accs = pickle.load(open("Accounts\Accs.p", "rb"))
                        accs[username] = hashlib.sha256(password.encode()).hexdigest()
                        pickle.dump(accs, open("Accounts\Accs.p", "wb"))

                        publics = pickle.load(open("Accounts\Keys\public.p", "rb"))
                        publics[username] = public
                        pickle.dump(publics, open("Accounts\Keys\public.p", "wb"))

                        privates = pickle.load(open("Accounts\Keys\private.p", "rb"))
                        index = hashlib.sha256((username+password).encode()).hexdigest()
                        privates[index] = private
                        pickle.dump(privates, open("Accounts\Keys\private.p", "wb"))

                        welcome = "y"
                        print("Account was created.\n")
                        break
                    print("Passwords do NOT match!\n")      
                    break
            return login()

        
        if welcome == "y":
            while True:
                login1 = input("\nLogin: ")
                login2 = input("Password: ")
                try:
                    accs = pickle.load(open("Accounts\Accs.p", "rb"))
                    
                    if accs[login1] == hashlib.sha256(login2.encode()).hexdigest():
                        print(f"\nWelcome {login1}")
                        return login1, login2
                except:
                    pass

                print("Incorrect username or password.\n")
                return login()

        if welcome != "y" and welcome != "n":
            print("\n")
            return login()
    else:
        username = acc[0]
        password = acc[1]
        try:
            if not(username in invalidNames or ", " in username):
                accs = pickle.load(open("Accounts\Accs.p", "rb"))
                accs[username]
            else: return
        except:
            public, private = keys()

            accs = pickle.load(open("Accounts\Accs.p", "rb"))
            accs[username] = hashlib.sha256(password.encode()).hexdigest()
            pickle.dump(accs, open("Accounts\Accs.p", "wb"))

            publics = pickle.load(open("Accounts\Keys\public.p", "rb"))
            publics[username] = public
            pickle.dump(publics, open("Accounts\Keys\public.p", "wb"))

            privates = pickle.load(open("Accounts\Keys\private.p", "rb"))
            index = hashlib.sha256((username+password).encode()).hexdigest()
            privates[index] = private
            pickle.dump(privates, open("Accounts\Keys\private.p", "wb"))

if __name__ == "__main__":
    account, password = login()
    print("\n"+account, password)