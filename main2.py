import random
import sys
import pyperclip
from collections import Counter
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*"
charsWithoutSpecialCharacter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
count = 20
CreateUser = "User.txt"
UserFile = "LoginDetails.txt"
file = ""
user = "AVIKYADAV"
passwd = "YouWillNeverGuessMySecretKey"
def CheckLogedFileForLogedIn(usr,pas):
    login = str(usr+" :-"+pas)
    print(login)
    with open(CreateUser,"r")as readable:
        data = readable.readlines()
        for line in data:
            print(line)
            str(line)
            if login in line:
                return True
                break
    return False
def CreateNewUser():
    with open(CreateUser,"a") as Create:
        inpt, passw = [i for i in input("enter user name and password you want to create separated by comma :").split(",")]
        print(inpt+" :-"+passw, file, file=Create)
        print("user Successfully created")
def SaveLoginDetails(user,passward):
    with open(UserFile,"a") as ueser:
        print(user," :-",passward,file,file=ueser)
def generatePassword(PasswordType)->"password":
    password = ""
    if PasswordType:
        for i in range(count):
            PasswordUnit = random.choice(chars)
            password = password+PasswordUnit
    return password
def CheckForDuplicateRecord(service):
    with open(file,"r") as f:
        data = f.readlines()
        for line in data:
            if service in line:
                print("you have a entered a service name that is already\n in your password safe means you have entered duplicate\nservice,",service)
                sys.exit("duplicate service name")
def logPassword(t):
    with open(file,"a") as passwd:
        Inp = input("for which service you want to create password")
        CheckForDuplicateRecord(Inp)
        Inp = Inp.lower()
        Inp = Inp.replace(" ","")
        print(Inp+" : "+generatePassword(t),file=passwd)
        pyperclip.copy(generatePassword(t))
        print("password Generated and copied to your clipboard successfully")
def RetrivePassword():
    with open(file) as passwd:
        print(passwd.read())
def Quit():
    sys.exit("sucessfully exited")
def deletePassword():
    found = False
    Inp = input("for which service you want to deletePassword password")
    with open(file, "r") as f:
        # read data line by line
        data = f.readlines()
    with open(file, "w") as f:

        for line in data:

            # condition for data to be deleted
            if Inp not in line:
                f.write(line)
            elif Inp in line:
                found = True
    if found ==False:
        print("No password found with given service")
    else:
        print("password Sucessfully deleted")
inpt, passw = [i for i in input("enter user name and password separated by comma :").split(",")]
re = CheckLogedFileForLogedIn(inpt,passw)

if re == True:
    file = inpt+".txt"
    SaveLoginDetails(inpt,passw)
    while True:
        print("***********************************\nq to quit\ns to store password\nr to retrive password\nd to delete password\n***********************************")
        Inp = input("enter What You wnat to do: ")
        if Inp == "q":
            Quit()
        if Inp =="s":
            Inp2 = input("do you want your password to contain special character \npress 1 for true \n2 for false\n")
            if Inp2 =="1":
                Inp2 = True
                logPassword(Inp2)
            if Inp2 =="2":
                Inp2 = False
                logPassword(Inp2)
        if Inp == "r":
             RetrivePassword()
        if Inp == "d":
            deletePassword()
else:
    print("login in failed,new user create your account")
    inpts = input("new user create your account\n for yes press 1\n for no press 2\n")
    if inpts =="1":
        CreateNewUser()