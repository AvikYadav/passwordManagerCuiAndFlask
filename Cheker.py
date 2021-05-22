from flask import session
from functools import wraps
def check_log_in(func):
    wraps(func)
    def wrapper(*args,**kwargs):
        if "login" in session:
            return func(*args,**kwargs)
        return "you are not loged in , this is resticted"

    wrapper.__name__ = func.__name__
    return wrapper