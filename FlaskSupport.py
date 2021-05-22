import random
import sys
import pyperclip
from Cheker import check_log_in
from flask import Flask,request,render_template,session
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
                session["login"] = True
                return True
                break
    return False
def CreateNewUser(inpt,passw):
    with open(CreateUser,"a") as Create:
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
def logPassword(t,Inp):
    with open(file,"a") as passwd:
        CheckForDuplicateRecord(Inp)
        Inp = Inp.lower()
        Inp = Inp.replace(" ","")
        print(Inp+" : "+generatePassword(t),file=passwd)
        pyperclip.copy(generatePassword(t))
        print("password Generated and copied to your clipboard successfully")
def RetrivePassword():
    with open(file) as passwd:
        ret = passwd.readlines()
        return ret
def Quit():
    sys.exit("sucessfully exited")
def deletePassword(Inp):
    found = False
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
def StorePassword(Inp,Inp2):
    with open(file,"a") as passwd:
        CheckForDuplicateRecord(Inp)
        print(Inp+" :-",Inp2,file=passwd)
        print("password stored successfully")

def USE():
    inpt, passw = [i for i in input("enter user name and password separated by comma :").split(",")]
    re = CheckLogedFileForLogedIn(inpt, passw)

    if re == True:
        file = inpt + ".txt"
        SaveLoginDetails(inpt, passw)
        while True:
            print(
                "***********************************\nq to quit\ns to store password\nr to retrive password\nd to delete password\n***********************************")
            Inp = input("enter What You wnat to do: ")
            if Inp == "q":
                Quit()
            if Inp == "s":
                Inp2 = input("do you want your password to contain special character \npress 1 for true \n2 for false\n")
                if Inp2 == "1":
                    Inp2 = True
                    logPassword(Inp2)
                if Inp2 == "2":
                    Inp2 = False
                    logPassword(Inp2)
            if Inp == "r":
                RetrivePassword()
            if Inp == "d":
                deletePassword()
    else:
        print("login in failed,new user create your account")
        inpts = input("new user create your account\n for yes press 1\n for no press 2\n")
        if inpts == "1":
            CreateNewUser()

app = Flask(__name__)

@app.route("/")
@app.route("/welcome")
def Start():
    return render_template("welcom.html",the_title = "welcome to password manager",
                           the_info="enter user/password")
@app.route("/process",methods= ["POST"])
def process():
    User = request.form["user"]
    Password = request.form["password"]
    if not User or not Password:
        return "Wrong Username,Password"
    re = CheckLogedFileForLogedIn(User,Password)
    if re == True:
        global file
        file = User + ".txt"
        SaveLoginDetails(User,Password)
        return render_template("Sucessfull.html",
                               the_title = "Login Successful Welcome to Password Manager "+User,
                               )
    else:
        return "Wrong Username,Password"
@app.route("/TakeCommand")
@check_log_in
def Command():
    command = "***********************************\ns to store password\ng to generate password\nr to retrive password\nd to delete password\n***********************************"
    return render_template("takeCommand.html",)

@app.route("/ProcessCommand",methods=["POST"])
def commandprocess():
    Inp = request.form["command"]
    if Inp == "g":
        return render_template("generate.html",
                               the_title = "enter the service name you want to generate password for")
    if Inp == "r":
        ret = RetrivePassword()
        return render_template("retrive.html",
                               the_title = "here are all your password",
                               data = ret)
    if Inp == "d":
        return render_template("delete.html",
                               the_title = "enter the service name you want to delete password for")
    if Inp == "s":
        return render_template("store.html",
                               the_title= "use this form to store your own password")
@app.route("/sucess")
def sucess():
    pass
@app.route('/createuser')
def create():
    return render_template("createuser.html",
                           the_title = "pls fill brlow form to create an account")
@app.route("/createprocess",methods= ["POST"])
def createprocess():
    usr = request.form["user"]
    passw = request.form["password"]
    CreateNewUser(usr,passw)
    return render_template("sucess.html")

@app.route("/GenerateProcess",methods=["POST"])
def generateprocess():
    Inp = request.form["command"]
    logPassword(True,Inp)
    return render_template("sucess.html",
                           the_title = "welcome to sucess.html")
@app.route('/logout')
def logout():
    session.pop('login')
    return "you are loged out in"
@app.route("/delete",methods= ["POST"])
def delete():
    dele = request.form["command"]
    deletePassword(dele)
    return render_template("sucess.html")
@app.route("/store",methods= ["POST"])
def store():
    use = request.form["command"]
    passw = request.form["passwd"]
    StorePassword(use,passw)
    return render_template("sucess.html")
app.secret_key="YouWillNeverGuessMySecretKey"
app.run(debug=True)


#use checker instaed for logining inimport random
import sys
import pyperclip
from Cheker import check_log_in
from flask import Flask,request,render_template,session
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
                session["login"] = True
                return True
                break
    return False
def CreateNewUser(inpt,passw):
    with open(CreateUser,"a") as Create:
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
def logPassword(t,Inp):
    with open(file,"a") as passwd:
        CheckForDuplicateRecord(Inp)
        Inp = Inp.lower()
        Inp = Inp.replace(" ","")
        print(Inp+" : "+generatePassword(t),file=passwd)
        pyperclip.copy(generatePassword(t))
        print("password Generated and copied to your clipboard successfully")
def RetrivePassword():
    with open(file) as passwd:
        ret = passwd.readlines()
        return ret
def Quit():
    sys.exit("sucessfully exited")
def deletePassword(Inp):
    found = False
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
def StorePassword(Inp,Inp2):
    with open(file,"a") as passwd:
        CheckForDuplicateRecord(Inp)
        print(Inp+" :-",Inp2,file=passwd)
        print("password stored successfully")

def USE():
    inpt, passw = [i for i in input("enter user name and password separated by comma :").split(",")]
    re = CheckLogedFileForLogedIn(inpt, passw)

    if re == True:
        file = inpt + ".txt"
        SaveLoginDetails(inpt, passw)
        while True:
            print(
                "***********************************\nq to quit\ns to store password\nr to retrive password\nd to delete password\n***********************************")
            Inp = input("enter What You wnat to do: ")
            if Inp == "q":
                Quit()
            if Inp == "s":
                Inp2 = input("do you want your password to contain special character \npress 1 for true \n2 for false\n")
                if Inp2 == "1":
                    Inp2 = True
                    logPassword(Inp2)
                if Inp2 == "2":
                    Inp2 = False
                    logPassword(Inp2)
            if Inp == "r":
                RetrivePassword()
            if Inp == "d":
                deletePassword()
    else:
        print("login in failed,new user create your account")
        inpts = input("new user create your account\n for yes press 1\n for no press 2\n")
        if inpts == "1":
            CreateNewUser()

app = Flask(__name__)

@app.route("/")
@app.route("/welcome")
def Start():
    return render_template("welcom.html",the_title = "welcome to password manager",
                           the_info="enter user/password")
@app.route("/process",methods= ["POST"])
def process():
    User = request.form["user"]
    Password = request.form["password"]
    if not User or not Password:
        return "Wrong Username,Password"
    re = CheckLogedFileForLogedIn(User,Password)
    if re == True:
        global file
        file = User + ".txt"
        SaveLoginDetails(User,Password)
        return render_template("Sucessfull.html",
                               the_title = "Login Successful Welcome to Password Manager "+User,
                               )
    else:
        return "Wrong Username,Password"
@app.route("/TakeCommand")
@check_log_in
def Command():
    command = "***********************************\ns to store password\ng to generate password\nr to retrive password\nd to delete password\n***********************************"
    return render_template("takeCommand.html",)

@app.route("/ProcessCommand",methods=["POST"])
def commandprocess():
    Inp = request.form["command"]
    if Inp == "g":
        return render_template("generate.html",
                               the_title = "enter the service name you want to generate password for")
    if Inp == "r":
        ret = RetrivePassword()
        return render_template("retrive.html",
                               the_title = "here are all your password",
                               data = ret)
    if Inp == "d":
        return render_template("delete.html",
                               the_title = "enter the service name you want to delete password for")
    if Inp == "s":
        return render_template("store.html",
                               the_title= "use this form to store your own password")
@app.route("/sucess")
def sucess():
    pass
@app.route('/createuser')
def create():
    return render_template("createuser.html",
                           the_title = "pls fill brlow form to create an account")
@app.route("/createprocess",methods= ["POST"])
def createprocess():
    usr = request.form["user"]
    passw = request.form["password"]
    CreateNewUser(usr,passw)
    return render_template("sucess.html")

@app.route("/GenerateProcess",methods=["POST"])
def generateprocess():
    Inp = request.form["command"]
    logPassword(True,Inp)
    return render_template("sucess.html",
                           the_title = "welcome to sucess.html")
@app.route('/logout')
def logout():
    session.pop('login')
    return "you are loged out in"
@app.route("/delete",methods= ["POST"])
def delete():
    dele = request.form["command"]
    deletePassword(dele)
    return render_template("sucess.html")
@app.route("/store",methods= ["POST"])
def store():
    use = request.form["command"]
    passw = request.form["passwd"]
    StorePassword(use,passw)
    return render_template("sucess.html")
app.secret_key="YouWillNeverGuessMySecretKey"
app.run(debug=True)


#use checker instaed for logining in