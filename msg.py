import os
from rsa.key import PrivateKey, PublicKey
from login import login
from rsa_crypto import encrypt, decrypt
import hashlib
import pickle
import time

ZONE = 1

def reset():
    """Resets the files and directories in the Messenger directory"""

    r = input("\nDo you really want to reset [YES]? ")

    if r == "YES":
        files = os.listdir("Messages")
        os.chdir("C:/Users/Paul Uni/Documents/Coding/Python/Blockchain/Messages")
        for i in files:
            os.remove(f"{i}")
        
        os.chdir("..")
        
        try:
            os.remove("Accounts/Accs.p")
            os.remove("Accounts/Keys/private.p")
            os.remove("Accounts/Keys/public.p")
        except:
            pass
        
        try: os.makedirs("Accounts")
        except: pass
        try: os.makedirs("Accounts/Keys")
        except: pass
        try: os.makedirs("Messages")
        except: pass
        os.chdir("C:/Users/Paul Uni/Documents/Coding/Python/Blockchain")
        print("Messenger reset succesfull")
    else:
        print("Shutting down...")

def timestamp():
    """Return a time stamp in the format DD.MM.YYYY HH:MM"""

    t = time.time()
    gm = time.gmtime(int(t))
    stamps = [(gm.tm_mday,2), (gm.tm_mon,2), (gm.tm_year,4), (gm.tm_hour+ZONE,2), (gm.tm_min,2)]
    fstamps = []
    
    for s in stamps:
        temp = str(s[0])
        if len(temp) == s[1]:
            pass
        else:
            while len(temp) != s[1]:
                temp = "0" + temp
        fstamps.append(temp)

    return f"{fstamps[0]}.{fstamps[1]}.{fstamps[2]} {fstamps[3]}:{fstamps[4]}"

class Messenger():
    def __init__(self) -> None:
        self.user, self.password = None, None
        login(("Admin", "1ks1#+5a8"))

    def manualLogin(self) -> None:
        """
        Transfers the Login to login, 
        creates the file for messages if not already created
        and sets the possible choose options
        """

        self.user, self.password = login()
        try:
            pickle.load(open(f"Messages/{hashlib.sha256((self.user).encode()).hexdigest()}.p", "rb"))
        except:
            pickle.dump([], open(f"Messages/{hashlib.sha256((self.user).encode()).hexdigest()}.p", "wb"))
        if self.user == "Admin":
            self.question = "What do you want to do?\nWrite Message\nRead Messages\nLogout\nLogout & Close\nReset\n-> "
        else:
            self.question = "What do you want to do?\nWrite Message\nRead Messages\nLogout\nLogout & Close\n-> "
        self.menu()

    def encryptMSG(self, msg: str, user: str) -> str:
        """Encrypts the given Message for every user in user seperated by ', '"""

        if self.user != None and self.password != None:
            try:
                publics = pickle.load(open("Accounts/Keys/public.p", "rb"))
                user = user.split(", ")

                if "All" not in user:
                    for receiver in user:
                        msgs = pickle.load(open(f"Messages/{hashlib.sha256((receiver).encode()).hexdigest()}.p", "rb"))

                        public = publics[receiver]
                        
                        prep_msg = f"{self.user} at {timestamp()}:\n"
                        e = encrypt(prep_msg+msg, public)

                        msgs.append(e)

                        pickle.dump(msgs, open(f"Messages/{hashlib.sha256((receiver).encode()).hexdigest()}.p", "wb"))
                else:
                    for public in publics:
                        msgs = pickle.load(open(f"Messages/{hashlib.sha256((public).encode()).hexdigest()}.p", "rb"))

                        prep_msg = f"{self.user} at {timestamp()}:\n"
                        e = encrypt(prep_msg+msg, publics[public])

                        msgs.append(e)

                        pickle.dump(msgs, open(f"Messages/{hashlib.sha256((public).encode()).hexdigest()}.p", "wb"))

                pickle.dump(msgs, open(f"Messages/{hashlib.sha256((self.user).encode()).hexdigest()}.p", "wb"))
                return "Message sent succesfully\n"

            except:
                return "User not found\n"
        else: self.manualLogin()
    
    def decryptMSG(self) -> list:
        """Decrypts the messages of the current user, if logged in"""

        if self.user != None and self.password != None:
            privates = pickle.load(open("Accounts/Keys/private.p", "rb"))
            private = privates[hashlib.sha256((self.user+self.password).encode()).hexdigest()]
            
            msgs = pickle.load(open(f"Messages/{hashlib.sha256((self.user).encode()).hexdigest()}.p", "rb"))

            for i in range(len(msgs)):
                msgs[i] = decrypt(msgs[i], private)

            return msgs
        else: self.manualLogin()
    
    def writeMessage(self) -> None:
        """Dispays the interface to write Messages"""

        if self.user != None and self.password != None:
            receiver = input("\nWho do you want to write? ")
            if receiver == "All" and self.user != "Admin":
                print("This Account is invalid.\n")
            else:
                msg = input("What do you want to write? ")
                c = input(f"You want to write \n'{msg}'\nto {receiver} [y]? ")

                if c == "y":
                    print(self.encryptMSG(msg, receiver))
                else:
                    print("Writing canceled.\n")
            self.menu()
        else: self.manualLogin()

    def readMessage(self) -> None:
        """Starts to read messages if a user is logged in"""

        if self.user != None and self.password != None:
            msgs = self.decryptMSG()

            print(f"\nYou have {len(msgs)} message(s):")
            i = None
            for i in msgs:
                print(i)
                current = msgs.index(i)
                if current != len(msgs) - 1:
                    print("---------------")
                else:
                    print("")
            if not(i):
                print("")
            self.menu()
        else: self.manualLogin()

    def logout(self, r=False) -> None:
        """Logs the current user out if one is logged in"""

        if self.user != None and self.password != None:
            self.user, self.password = None, None
            print("You logged out.")

            if not(r):
                print("")
                self.manualLogin()
                self.menu()
            
        else: self.manualLogin()
    
    def menu(self):
        """Displays a Menu and links the answer to the correct Funktion"""

        if self.user != None and self.password != None:
            i = input(self.question)
            if i == "Write Message":
                self.writeMessage()
            elif i == "Read Messages":
                self.readMessage()
            elif i == "Logout":
                self.logout()
            elif i == "Logout & Close":
                self.logout(True)
            elif i == "Reset" and self.user == "Admin":
                i = input("\nIn order to do so, please enter the MasterKey: ")
                if i == "1ks1#+5a8":
                    self.logout(True)
                    reset()
                    login(("Admin", "1ks1#+5a8"))
            else: 
                print("")
                self.menu()
        else: self.manualLogin()

if __name__ == "__main__":
    M = Messenger()
    M.manualLogin()