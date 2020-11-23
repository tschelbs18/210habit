import requests

BASE = "http://127.0.0.1:5000/"

data = [{"habit_name":"Jogging"},{"habit_name":"Not drinking soda"},{"habit_name":"Reading"}]
for i in range(len(data)):
    response = requests.put(BASE + "habits/" + str(i),data[i]);
    print(response.json())

input()
response = requests.delete(BASE + "habits/0")
print(response)
