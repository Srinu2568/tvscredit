import os

from deta import Deta
from dotenv import load_dotenv

load_dotenv('.env')

DETA_KEY = os.getenv('DETA_KEY') # Load the deta key from .env file

# Initialzie deta object with a project key

deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base('user_db')

def insert_user(username, name, password, isEval=False, form_data=[], type_data=[]):
    """"Returns the user on a successful user creation, otherwise raises an error"""
    return db.put({'key':username, 'name':name, 'password': password, 'isEval':isEval, 'images':[], 'form_data':form_data, 'type_data':type_data})

# To insert the users in the database
# insert_user('user', 'user1', 'abc123', False)

# Returns the instance of fetch response class
def fetch_all_users():
    """Returns a dict of all users"""
    res = db.fetch()
    return res.items # res.count, res.list


# To print all the users
# print(fetch_all_users())

def get_user(username):
    """If not found, the function will return None"""
    return db.get(username)
# print(get_user('pparker'))

def update_user(username, updates):
    """If the item is updated, returns None. Otherwise, an exception is raised"""
    return db.update(updates, username)
# update_user('pparker', updates={'name': 'Spider Man'})

def delete_user(username):
    """Always returns None, even if the key does not exist"""
    return db.delete(username)
# delete_user('user') # To delete user