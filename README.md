# 210habit
Habit and Activity Tracker Web App for CSE210

## Getting Started ##

1. Install Python 3

2. Initialize a virtual environment (this will keep installed files within the virtual environment, not affecting the global python libraries)

`python -m venv env`

*Note: this may hang for a few seconds*

3. Install the required modules into your virtual environment
`pip install -r requirements.txt`

4. Test the application
[todo] `python test/*`

5. Run the server
`python application.py`

6. Verify the server is working
in your browser, visit 127.0.0.1:5000.

## REST API ##
### Return the habits associated with that user###
GET /api/habits/<username>  
<!-- Q: is user name unique? identifier?
session token?
 -->
Response: 200 OK on success
{"habits": ["Jogging", "not drinking soda"]}

### Add a new habit ###
POST /api/habits/<new_activity>
Arguments:
```
{
	"activity": "new activity name"
}
```
Response: 201 Created on success
```
{
	"activity_id": "string a globally unique identifier for this activity",
	"username": "user name for this user",
	"activity" : "new activity name"
}
```
### Delete activity ###
DELETE /api/habit/<activity>
Response: 200 Delete successful
204 No content

### Return the logs associated with that activity###
GET /api/habits/logs/<activity>
Optional arguments: start day and end day
Response: 200 OK on success
```
{"active_days": ["YYYY-MM-DD"]}
```
### Add data to an activity entry ###
POST /api/habits/logs/
Arguments:
```
{
	"activity_id": "string a globally unique identifier for this activity",
	"day_to_log": "YYYY-MM-DD"
}
```
Response: 201 Created on success

### User login ###
POST /login
<!-- use email? -->
Arguments:
```
{
	"username": "",
	"password": "salt + hashed password"
}
```
Response:
200 The authentication was successful. The response will contain the user token that was authenticated.
```
{
	"message": "Auth successful",
	"token": ""
}
```
404 The user was not found or the password was incorrect. The response will be empty.

### Create a new user ###
POST /api/users
Arguments:
```
{
	"username": "new user name",
	"password": "salt + hashed password"
}
```
Response: 201 Created on success
500 Created failed

### Render login page  ###
GET /login

### Render habits page  ###
GET /habits

### Render progress page  ###
GET /progress
