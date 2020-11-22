window.render_streak = (streak, DOMCell, $cell) => {
	return "&#x1F525; " + String(streak)
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
		//this.habits = [];
		// temporary while testing
		this.habits = ["Running", "Working Out", "Eating Vegetables"];
		this.streaks = {"Running":13, "Working Out":7, "Eating Vegetables":2}
		this.session_id = session_id;
		this.user = user;
		this.zg = zg;
	}

	/**
	 * Retrieves a user's list of habits from the server, storing them internally.
	 * @requestHabits
	 */
	requestHabits()
	{
		var mgr = this;
		fetch('http://127.0.0.1:8080/api/habits/', {credentials: 'include'})
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
	 * Adds or deletes the user's habit from the server.
	 * @updateHabit
	 * @param {string} habit - the name of the habit to delete
	 * @param {string} action - either 'add' or 'delete' the habit
	 */
	updateHabit(habit, action)
	{
		var mgr = this;
		fetch('http://127.0.0.1:8080/api/habits/', {
			method: 'post',
			headers: {
			  "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
			},
			credentials: 'include',
			body: 'habit='+habit+'&action='+action+'&user='+mgr.user+'&session_id='+mgr.session_id
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
		var mgr = this;
		console.log("Updating rows with habits: "+this.habits);
		var data = [];
		for(var i = 0; i < this.habits.length; i++)
		{
			data.push({'habit':this.habits[i], 'streak':this.streaks[this.habits[i]]});
		}
		this.zg.setData(data);

		// update the callback handlers
		var log_buttons = document.getElementsByClassName('log-button');
		for (i=0; i < log_buttons.length; i++)
		{
			log_buttons[i].addEventListener("click", function(e) {
				console.log(e.target);
				var button = e.target;
		
				if(button.className != "log-button")
				{
					button = button.parentElement; // checkmark or text element in button target
				}

				button.disabled = true;
				var habit = button.parentElement.parentElement.nextElementSibling.textContent;
				console.log("Log clicked for habit: " + habit);
				mgr.logHabit(habit);
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
		fetch('http://127.0.0.1:8080/api/habits/log', {
			method: 'post',
			headers: {
			  "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
			},
			credentials: 'include',
			body: 'date='+timestamp+'&user='+mgr.user+'&session_id='+mgr.session_id
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

	zgRef.addEventListener('data:record:delete', (e) => {
		console.log('Habit deleted: ' + e.detail.ZGData.data.habit);
		manager.updateHabit(e.detail.ZGData.data.habit, 'delete');
	});

	zgRef.addEventListener('data:record:create', (e) => {
		console.log('Habit created: ' + e.detail.ZGData.data.habit);
		manager.updateHabit(e.detail.ZGData.data.habit, 'add');
	});
});