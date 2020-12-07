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
  // Sort the habitList alphabetically
  const orderedHabitList = {};
  Object.keys(habitList).sort().forEach(function(key) {
    orderedHabitList[key] = habitList[key];
  });

  // Loop over the array of habits and add a header and chart.
  for (var habitname of Object.keys(orderedHabitList)) {
    // Create a header element with the name of the habit
    var header = document.createElement("H2");
    var headerText = document.createTextNode(habitname);
    header.appendChild(headerText);
    root.appendChild(header);
    // Create a div element in which to render that habit's chart and set the id to the name of the habit
    var div = document.createElement("div");
    div.setAttribute("id", habitname);
    root.appendChild(div);
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
    /* adds day labels to calender boxes
       plot: {
      valueBox: { // Use this object to configure the value boxes.
      }
    } */
  };
  // Render the ZingChart with the habit name for the respective div ID and current config of data.
  zingchart.render({
    id: habitname,
    data: myConfig,
    height: 250,
    width: '60%'
  });
  }
}
