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

	button.disabled = true;
	button.removeEventListener(e.type, handler);
	var habit = button.parentElement.parentElement.nextElementSibling.textContent;
	var streak = button.parentElement.parentElement.nextElementSibling.nextElementSibling;
	var new_streak = parseInt(streak.getAttribute('value')) + 1;
	streak.setAttribute('value',new_streak.toString());
	streak.innerHTML = "🔥 " + new_streak;
	
	manager.logHabit(habit);
}

/** This class manages retrieving habits from the server and rendering them in a Zing Grid on the page. */
class HabitManager {
	/**
	 * Managers habit requests and updates to the server.
	 * @constructor
	 * @param {string} session_id - The session id of the current user
	 * @param {string} user - The current user
	 * @param {ZingGrid} zg - The zing grid object
	 */
	constructor(session_id, user, zg) {
		// temporary while testing
		this.session_id = session_id;
		this.user = user;
		this.zg = zg;
		this.renderRows = this.renderRows.bind(this)
		this.habits = [];
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

				document.getElementById('loader-page').style.display='none';
				document.getElementById('loader-spinner').style.display='none';

			  if (response.status !== 200) {
				console.log('Looks like there was a problem. Status Code: ' +
				  response.status);
				return;
			  }

			  // Examine the text in the response
			  response.json().then(function(data) {
				console.log(data);
				mgr.habits = data.habits;
				mgr.streaks = data.streaks; //tbd determine format of streaks in endpoint
				mgr.renderRows(); // due to async nature, we call here
			  });
			}
		  )
		  .catch(function(err) {
			console.log('Fetch Error :-S', err);

				document.getElementById('loader-page').style.display='none';
				document.getElementById('loader-spinner').style.display='none';

				// temporary while testing
				mgr.renderRows();
		  });
		

	}

	/**
	 * Adds the user's habit to the server.
	 * @addHabit
	 * @param {string} habit - the name of the habit to add
	 */
	addHabit(habit)
	{
		console.log("attempting to add habit: " + habit);
		var mgr = this;
		fetch('http://127.0.0.1:5000/api/habits', {
			method: 'post',
			headers: {
			  "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
			},
			credentials: 'include',
			body: 'habitname='+habit+'&user='+mgr.user+'&session_id='+mgr.session_id
		  })
		  .then(
			function(response) {
				if (response.status !== 201) {
				console.log('Looks like there was a problem. Status Code: ' +
				  response.status);
					return;
				}

				var zg = document.querySelector('zing-grid');
				zg.insertRow({
					"habit": habit,
					"streak": 0
				});
		  })
		  .catch(function (error) {
			console.log('Request failed', error);
			// test only, add anyways:
			var zg = document.querySelector('zing-grid');
			zg.insertRow(        {
				"habit": habit,
				"streak": 0
			});
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
		fetch('http://127.0.0.1:5000/api/habits/'+habit, {
			method: 'delete',
			headers: {
			  "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
			},
			credentials: 'include',
			body: 'user='+mgr.user+'&session_id='+mgr.session_id
		  })
		  .then(
			function(response) {
				if (response.status !== 200) {
				console.log('Looks like there was a problem. Status Code: ' +
				  response.status);
				return;
				}

				response.json().then(function(data) {
					console.log('Request succeeded with JSON response', data);
				});
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
		// this.habits = [];
		console.log("Updating rows with habits: "+this.habits);
		var mgr = this;
		var data = [];
		for(var i = 0; i < this.habits.length; i++)
		{
			data.push({'habit':this.habits[i], 'streak':this.streaks[i]});
		}
		this.zg.setData(data);

		// update the callback handlers
		var log_buttons = document.getElementsByClassName('log-button');
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
		let today = new Date()
		var timestamp = today.toISOString().split('T')[0] // YYYY-MM-DD format
		var mgr = this;
		fetch('http://127.0.0.1:5000/api/habits/log', {
			method: 'post',
			headers: {
			  "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
			},
			credentials: 'include',
			body: 'day_to_log='+timestamp+'&habit_name='+habit+'&user='+mgr.user+'&session_id='+mgr.session_id
		  })
		  .then(
			function(response) {
				if (response.status !== 200) {
				console.log('Looks like there was a problem. Status Code: ' +
				  response.status);
				return;
				}

				response.json().then(function(data) {
					console.log('Request succeeded with JSON response', data);
				});
		  })
		  .catch(function (error) {
			console.log('Request failed', error);
		  });
	}
}

window.addEventListener('load', (event) => {
	const zgRef = document.querySelector('zing-grid');

	let manager = new HabitManager('0','user',zgRef);

	zgRef.executeOnLoad(function() {
		manager.requestHabits();
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
		if(input.value != '')
		{
			document.getElementById('loader-page').style.display='block';
			document.getElementById('loader-spinner').style.display='block';
			manager.addHabit(input.value);
		}
	});
});