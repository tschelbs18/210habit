# 210habit ![Python application](https://github.com/tschelbs18/210habit/workflows/Python%20application/badge.svg) ![Jest Tests](https://github.com/tschelbs18/210habit/workflows/Jest%20Tests/badge.svg)
Habit and Activity Tracker Web App for CSE210

## Getting Started ##
*Note: We recommend using Chrome as the browser for using this application for the best experience*

1. Install Python 3

2. Initialize a virtual environment (this will keep installed files within the virtual environment, not affecting the global python libraries) in the 210 habit branch root directory

`python -m venv env`

*Note: this may hang for a few seconds*

3. Activate your virtual environment
On Windows: `env\scripts\activate`
On Mac: `source env/bin/activate`

3. Install the required modules into your virtual environment
`pip install -r requirements.txt`

4. Test the application
`pytest --ignore=test/test__selenium_habit.py --ignore=test/test__selenium_login.py`

*Note: we ignore running end-to-end tests by default as they require the chromedriver to be setup on your local machine, however they are run by the repo CLI*


5. Run the server
`python app.py`

6. Verify the server is working
in your browser, visit 127.0.0.1:5000.


## REST API ##
### Return the habits associated with that user ###
GET /api/habits  
Response: 200 OK on success
{"habits": ["Jogging", "not drinking soda"]}

### Add a new habit ###
POST /api/habits/<new_habit>
Arguments:
```
{
	"activity": "new habit name"
}
```
Response: 201 Created on success
```
{
	"username": "user name for this user",
	"habit" : "new habit name"
}
```
### Delete habit ###
DELETE /api/habit/<habit_name>
Response: 200 Delete successful
204 No content

### Return the logs associated with that habit ###
GET /api/habits/logs/<habit>
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
	"habit_name": "name for this activity",
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
## Documentation ##
For additional documentation on underlying code, check out the "docs" directory.
