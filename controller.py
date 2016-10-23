from flask import Flask
from model import create_user,get_user
app = Flask(__name__)


def create_account(_name,_email,_password): #creates user in the database
    return create_user(_name,_email,_password)

def validate_user(_username): #checks that user exists
    return get_user(_username)
