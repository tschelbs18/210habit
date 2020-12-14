test('Verify create habit button callback fires on nonempty input', async () => {

	const fs = require('fs');
	const path = require('path');
	const html = fs.readFileSync(path.resolve(__dirname, '../../templates/habits.html'), 'utf8');

	// Set up our document body
	document.body.innerHTML = html;

	// manager mock
	const manager = {
	  addHabit(habit) {
		return true;
	  },
	};

	// code from log.js (should be reference to actual imported func)
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

	const spy = jest.spyOn(manager, 'addHabit');

	expect(spy).not.toHaveBeenCalled();
	
	var habit_input = document.getElementById('new-habit');
	
	habit_input.value = '';
	
	btn.click();
	
	expect(spy).not.toHaveBeenCalled();	
	
	habit_input.value = 'test';
	
	btn.click();
	
	expect(spy).toHaveBeenCalled();

});