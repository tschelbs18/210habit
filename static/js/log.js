window.render_streak = (streak, DOMCell, $cell) => {
	return "&#x1F525; " + String(streak)
}

function log_callback(handler, manager, e)
{
	var button = e.target;

	while(!button.className.includes("log-button"))
	{
		button = button.parentElement; // checkmark or text element in button target
	}

	if(button.disabled)
	{
		button.removeEventListener(e.type, handler);
	}
	else
	{
		button.disabled = true;
		button.removeEventListener(e.type, handler);
		var habit = button.parentElement.parentElement.nextElementSibling.textContent;
		var streak = button.parentElement.parentElement.nextElementSibling.nextElementSibling;
		var new_streak = parseInt(streak.getAttribute('value')) + 1;
		streak.setAttribute('value',new_streak.toString());
		streak.innerHTML = "🔥 " + new_streak;

		manager.logHabit(habit);
	}
}

/** This class manages retrieving habits from the server and rendering them in a Zing Grid on the page. */
class HabitManager {
	/**
	 * Managers habit requests and updates to the server.
	 * @constructor
	 */
	constructor() {
		this.habits = [];
		this.streaks = {};
	}

	/**
	 * Retrieves a user's list of habits from the server, storing them internally.
	 * @requestHabits
	 */
	requestHabits()
	{
		var mgr = this;
		fetch('http://127.0.0.1:5000/api/habits', {credentials: 'include'})
		  .then(
			function(response) {
			  if (response.status !== 200) {
					console.log('Looks like there was a problem. Status Code: ' +
				  response.status);
				return;
			  }

			  // Examine the text in the response
			  response.json().then(function(data) {
				console.log(data);
				mgr.habits = data.habits;
				var i;
				for(i = 0; i < mgr.habits.length; i++)
				{
					mgr.streaks[data.habits[i]] = data.streaks[i];
				}
				mgr.habits.sort(); // render habits in alphabetical order
				mgr.renderRows(); // due to async nature, we call here
			  });
			}
		  )
		  .catch(function(err) {
			console.log('Fetch Error :-S', err);
		  });
	}

	/**
	 * Adds the user's habit to the server.
	 * @addHabit
	 * @param {string} habit - the name of the habit to add
	 */
	addHabit(habit)
	{
		var mgr = this;
		console.log(mgr.habits);
		if(mgr.habits.indexOf(habit) != -1)
		{
			// warn habit already exists
			console.log("Duplicate habit ignored!");
			return;
		}
		document.getElementById('loader-page').style.display='block';
		document.getElementById('loader-spinner').style.display='block';
		console.log("attempting to add habit: " + habit);
		fetch('http://127.0.0.1:5000/api/habits', {
			method: 'post',
			headers: {
			  "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
			},
			credentials: 'include',
			body: 'habitname='+habit
		  })
		  .then(
			function(response) {
				if (response.status !== 201) {
				console.log('Looks like there was a problem. Status Code: ' +
				  response.status);
				document.getElementById('loader-page').style.display='none';
				document.getElementById('loader-spinner').style.display='none';
					return;
				}

				var zg = document.querySelector('zing-grid');
				zg.insertRow({
					"habit": habit,
					"streak": 0
				});

				mgr.habits.push(habit);
		  })
		  .catch(function (error) {
			console.log('Request failed', error);
		  });
	}

	/**
	 * Deletes the user's habit from the server.
	 * @deleteHabit
	 * @param {string} habit - the name of the habit to delete
	 */
	deleteHabit(habit)
	{
		var mgr = this;
		fetch('http://127.0.0.1:5000/api/habits', {
			method: 'delete',
			headers: {
			  "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
			},
			credentials: 'include',
			body: 'habitname='+habit
		  })
		  .then(
			function(response) {
				if (response.status !== 200) {
				console.log('Looks like there was a problem. Status Code: ' +
				  response.status);
				return;
				}

				console.log('Successfully delete habit:', habit);
				mgr.habits.pop(habit);
		  })
		  .catch(function (error) {
			console.log('Request failed', error);
		  });
	}

	/**
	 * Renders the user's habits from the server in the Zing Grid.
	 * @renderRows
	 */
	renderRows()
	{
		console.log("Updating rows with habits: "+this.habits);
		var mgr = this;
		var data = [];
		for(var i = 0; i < this.habits.length; i++)
		{
			data.push({'habit':this.habits[i], 'streak':this.streaks[this.habits[i]]});
		}
		var zg = document.querySelector('zing-grid');
		zg.setData(data);

		// update the callback handlers
		var log_buttons = document.getElementsByClassName('log-button');
		console.log(log_buttons);
		for (i=0; i < log_buttons.length; i++)
		{
			log_buttons[i].addEventListener("click", function handler(e) {
				log_callback(handler, mgr, e);
			});
		}
	}

	/**
	 * Updates the user's habit log on the server with the given habit.
	 * @logHabit
	 * @param {string} habit - the name of the habit to log
	 */
	logHabit(habit)
	{
		var mgr = this;
		let today = new Date();
		var localOffset = today.getTimezoneOffset() * 60000;
		var localTime = today.getTime();
		today = new Date(localTime - localOffset);
		var timestamp = today.toISOString().split('T')[0] // YYYY-MM-DD format
		fetch('http://127.0.0.1:5000/api/habits/logs', {
			method: 'post',
			headers: {
			  "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
			},
			credentials: 'include',
			body: 'habitname='+habit+'&day_to_log='+timestamp
		  })
		  .then(
			function(response) {
				if (response.status !== 200) {
					console.log('Looks like there was a problem. Status Code: ' +
					response.status);
					return;
				}
				mgr.streaks[habit] += 1;
				console.log('Successfull activity post:', habit, timestamp);
		  })
		  .catch(function (error) {
			console.log('Request failed', error);
		  });
	}
}

async function requestHabitLogs()
{
  let response = await fetch('http://127.0.0.1:5000/api/habits/all_logs', {credentials: 'include'});
  let data = await response.json();
  return data;
}

window.addEventListener('load', (event) => {
	const zgRef = document.querySelector('zing-grid');

	let manager = new HabitManager();

	zgRef.executeOnLoad(async function() {
		manager.requestHabits();

		// request habit logs to ensure we disable the log button
		var habitList = await requestHabitLogs();

		let today = new Date();
		var localOffset = today.getTimezoneOffset() * 60000;
		var localTime = today.getTime();
		today = new Date(localTime - localOffset);
		var timestamp = today.toISOString().split('T')[0]; // YYYY-MM-DD format

		var already_logged = [];
		for (var habitname of Object.keys(habitList)) {
			dates = habitList[habitname];
			if(dates.length > 0)
			{
				var most_recent_log = dates[dates.length-1][0];
				if(most_recent_log == timestamp)
				{
					console.log('already logged today: '+habitname);
					already_logged.push(habitname);
				}
			}
		}

		console.log("Already logged: " + already_logged);

		await new Promise(resolve => setTimeout(resolve, 100));

		habits = [];
		log_buttons = [];
		//iterate over all habits, pulling the habit values
		var habit_rows = document.querySelectorAll("zg-cell[aria-colindex='1']");
		habit_rows.forEach(function(habit_row) {
			habits.push(habit_row.textContent);
			log_buttons.push(habit_row.previousElementSibling.firstElementChild.firstElementChild);
		});

		already_logged.forEach(function(habit) {
			var button_to_disable = habits.indexOf(habit);
			if(button_to_disable != -1) {
				console.log(button_to_disable);
				log_buttons[button_to_disable].disabled = true;
			}
		});

		document.getElementById('loader-page').style.display='none';
		document.getElementById('loader-spinner').style.display='none';
	});

	// Customize delete record dialog
	zgRef.customizeDialog('record-delete', {
	  cancel: "Cancel",
	  confirm: "Delete Habit",
	  label: "Confirm permanently deleting habit"
	});

	zgRef.addEventListener('data:record:delete', (e) => {
		console.log('Habit deleted: ' + e.detail.ZGData.data.habit);
		manager.deleteHabit(e.detail.ZGData.data.habit);
	});

	zgRef.addEventListener('data:record:insert', async (e) => {
		console.log('Habit created: ' + e.detail.ZGData.data.habit);
		document.getElementById('loader-page').style.display='none';
		document.getElementById('loader-spinner').style.display='none';
		await new Promise(resolve => setTimeout(resolve, 500)); // wait for new log row to be added
		var log_buttons = document.getElementsByClassName('log-button');
		log_buttons[log_buttons.length - 1].addEventListener("click", function handler(e) {
				log_callback(handler, manager, e);
		});
	});

	// bind callback for create new habit button
	var btn = document.getElementById('add');
	btn.addEventListener("click", function add(e) {
		var input = document.getElementById('new-habit');
		var new_habit = input.value;
		new_habit = new_habit.replace(/(^[ '\^\$\*#&]+)|([ '\^\$\*#&]+$)/g, '') // strip whitespace
		if(new_habit != '')
		{
			manager.addHabit(new_habit);
			input.value = '';
		}
	});
});
