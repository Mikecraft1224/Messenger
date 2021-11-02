# Messenger
This is a small messenger with the cmd as an interface.  
It started as a project to learn more about Python 3.  
  
If you want to run a version of this messenger, please copy the venv folder in the folder  
of the version you want, because I don't want to fill this repo with 20MBs of venv for every  
version when there is just 1GB of space available.  
Then just open "start.bat"  

---
### Features:
- create an account and login
- pre-created user "Admin" with access to complete reset, the password is 1ks1#+5a8 and is just for  
  testing purposes
- store only the passwords hash
- not even the Admin can read messages, due to them stored anonimously,  
  at the time just possible with trial and error when trying all PrivateKeys
- read messages, write messages to other users, Admin can use "All" to write to every account
- saves RSA-encrypted messages for better safety
---

### Next steps for the messenger:
- better security for the messages  
  --> encrypt PrivateKey with a variant and/or hash of the password
- add serverversion, which sends data to a website to display
- add add desktopversion with GUI, which gets data from a server
- add a batch in order to set settings
---

For bugs and requested features please contact MARS#5949 on discord or Mikecraft1224@gmail.com via E-Mail
