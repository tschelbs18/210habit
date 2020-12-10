/**
  * On page load, load the ZingChart Calendar Library immediately.
  * Then render the charts.
*/
window.onload = function() {
  zingchart.MODULESDIR = 'http://cdn.zingchart.com/modules/';
  zingchart.loadModules('calendar', function() {
    renderHabitCharts();
  });
};

/**
 * Return an object with the relevant dates needed to build a T3M calendar.
 * @param {date} today - Today's date.
*/
function getRelevantDates(today) {
  // Return the current year in YYYY string format, start and end month of the calendar view as integers.
  // End month is the current month
  // Get current Month as MM
  var mm = today.getMonth() + 1;
  // Starting month is 1 if current month is <= 2 otherwise it is 2 months prior to current month
  if (mm <= 2) {
    var startMonth = 1;
  } else {
    var startMonth = mm - 2;
  }
  return {'year': String(today.getFullYear()),
    'startMonth': startMonth,
    'endMonth': mm,
  };
}

/**
 * Perform an API call to get the habit activity for the current user.
*/
async function requestHabits()
{
  let response = await fetch('http://127.0.0.1:5000/api/habits/all_logs', {credentials: 'include'});
  let data = await response.json();
  return data;
}

/**
 * Takes the results of getRelevantDates and requestHabits to build a T3M chart for each of the habits logged for the current user.
*/
async function renderHabitCharts() {
  // Render the relevant charts for the user's habit activity over the most recent 3 months.
  // Get the habit information for the current user.
  var habitList = await requestHabits();
  // Get the needed date information to build the calendar.
  var dates = getRelevantDates(new Date());
  // Get root node within which we will insert new html elements.
  var root = document.getElementById('zing-placeholder');
  
  // Handle the case that the user has no habits yet.
  if (habitList.length == 0) {
    // Add a header specifying no habits yet added to the DOM.
    var header = document.createElement("H2");
    var headerText = document.createTextNode("No habits yet added.");
    header.appendChild(headerText);
    root.appendChild(header);
  }

  // turn streaks for each activity into scaled color values
  for (const [_, activities] of Object.entries(habitList)) {
    var max_streak = activities[0][1];
    for (i = 0; i < activities.length; i++) {
      if (max_streak < activities[i][1]) {
        max_streak = activities[i][1];
      }
    }
    for (i = 0; i < activities.length; i++) {
      activities[i][1] = 6*activities[i][1]/max_streak+1
    }
  }
  
  // Sort the habitList alphabetically
  const orderedHabitList = {};
  Object.keys(habitList).sort().forEach(function(key) {
    orderedHabitList[key] = habitList[key];
  });

  var habit_names = [];
  var habit_ids = [];

  // Loop over the array of habits and add a header and chart.
  for (var habitname of Object.keys(orderedHabitList)) {
    // create labeled container for the habit
	var habitname_clean = habitname.replaceAll(' ','_');
	habitname_clean = habitname_clean.toLowerCase();
	habit_names.push(habitname)
	var habit_div = document.createElement("div");
	habit_div.id = habitname_clean + "_wrapper"
	habit_div.classList.add("habit-rendered");
	habit_ids.push(habit_div.id)
	habit_div.style.display = 'none';
	root.appendChild(habit_div);
    // Create a header element with the name of the habit
    var header = document.createElement("H2");
    var headerText = document.createTextNode(habitname + " Progress");
    header.appendChild(headerText);
    habit_div.appendChild(header);
    // Create a div element in which to render that habit's chart and set the id to the name of the habit
    var div = document.createElement("div");
    div.setAttribute("id", habitname_clean);
    habit_div.appendChild(div);
    // Build a context dictionary for configuring the chart
    var myConfig = {
    type: 'calendar',
    options: {
      startMonth: dates['startMonth'], //Set the starting month (1-12).
      endMonth: dates['endMonth'],
      year: {
        text: dates['year'],
        visible: true
      },
      values: orderedHabitList[habitname]
    },
     // pads spacing around the chart
     plotarea: {
      marginTop: '20%',
      marginBottom:'20%',
      marginLeft:'10%',
      marginRight:'10%'
    },
    // tooltip: {
    //   visible: false
    // }
    /* adds day labels to calender boxes
       plot: {
      valueBox: { // Use this object to configure the value boxes.
      }
    } */
  };
  // Render the ZingChart with the habit name for the respective div ID and current config of data.
  zingchart.render({
    id: habitname_clean,
    data: myConfig,
    height: 250,
    width: '60%'
  });
  }
  
  // populate the dropdown with the habit names/ids
    var select = document.getElementById("habit-select");
  var i;
  for(i = 0; i < habit_names.length; i++)
  {
	var option = document.createElement("option");
	option.value = habit_ids[i];
	option.text = habit_names[i];
	select.appendChild(option);
  }
  
  // show the first elem by default
  var rendered = document.getElementsByClassName('habit-rendered');
  rendered[0].style.display = 'block';
  
  // add the selection dropdown handler
  select.addEventListener('change', function(e){
	var elem = e.target; 
    var idx  = elem.selectedIndex;
    var habit_sel = elem.options[idx].value;

	// hide all previous
	var rendered = document.getElementsByClassName('habit-rendered');
	var i;
	for(i = 0; i < rendered.length; i++)
	{
		rendered[i].style.display = 'none';
	}
	
	var showHabit = document.getElementById(habit_sel);
	showHabit.style.display = 'block';
  });
  
	document.getElementById('loader-page').style.display='none';
	document.getElementById('loader-spinner').style.display='none';
  
}
