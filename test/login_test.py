import requests
import json

def register():
    user = {'username':'zren@ucsd.edu', 'password':'1234567'}
    s = json.dumps(user)
    data = requests.post( url='http://127.0.0.1:5000/register', json = user)
    print(data.text) 

def login():
    user = {'username':'zren@ucsd.edu', 'password':'1234567'}
    s = json.dumps(user)
    data = requests.post( url='http://127.0.0.1:5000/login', json = user)
    print(data.text)

def logout():
    user = {'username':'zren@ucsd.edu', 'password':'1234567'}
    s = json.dumps(user)
    data = requests.post(url='http://127.0.0.1:5000/login', json = user)
    print(data.text)
    data = requests.post(url='http://127.0.0.1:5000/logout')
    print(data.text)

if __name__ == '__main__':
    register()
    login()
    logout()