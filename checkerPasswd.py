from functools import wraps
from flask import session,request
passwd = "YouWillNeverGuessMyPassword"
def CheckPassword(func):
    wraps(func)
    def Check(*args,**kwargs):
        passwdEntered = request.form["Password"]
        if passwdEntered == passwd:
            return func(*args,**kwargs)
        return "password Incorrect"

    Check.__name__ = func.__name__
    return Check