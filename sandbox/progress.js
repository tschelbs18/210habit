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
function requestHabits() {
  // var xhr = new XMLHttpRequest();
  // xhr.open('GET', 'https://api.CSE210habit.com/user/habits', true);
  /*
  Notes:
  Order doesn't matter for the dates, but value does for the opacity of the color.
  - Should confirm that only 1s or 0s are coming into the values. Maybe build some logic to handle non-binary date_values
  - T30D view for multiple months?
  */
  // Single habit, all in one month
  var user1habits = [
    {
      'name': 'Running',
      'date_values': [
        ['2020-11-01', 1],
        ['2020-11-02', 1],
        ['2020-11-05', 1],
        ['2020-11-08', 1],
        ['2020-11-09', 1],
        ['2020-11-14', 1],
        ['2020-11-16', 1],
        ['2020-11-30', 1],
        ['2020-11-18', 1],
        ['2020-11-29', 1],
      ],
    }
  ];
  // Multiple Habits with different date ranges and no data
  var user2habits = [
    {
      'name': 'Running',
      'date_values': [
        ['2020-10-01', 1],
        ['2020-10-02', 1],
        ['2020-10-05', 1],
        ['2020-11-08', 1],
        ['2020-11-18', 1],
        ['2020-11-29', 1],
      ],
    },
    {
      'name': 'Reading',
      'date_values': [
        ['2020-09-01', 1],
        ['2020-09-09', 1],
        ['2020-11-25', 1],
        ['2020-10-11', 1],
        ['2020-10-14', 1],
        ['2020-10-17', 1],
      ],
    },
    {
      'name': 'Meditating',
      'date_values': [
        ['2020-11-01', 1],
        ['2020-11-02', 1],
        ['2020-11-05', 1],
        ['2020-11-08', 1],
        ['2020-09-18', 1],
        ['2020-10-29', 1],
      ]
    },
    {
      'name': 'Napping',
      'date_values': [
      ]
    }
  ];
  // Illogical inputs
  var user3habits = [
    {
      'name': 'Running',
      'date_values': [
        ['xxxx-11-02', 1],
        ['2020-11-09', 1],
        ['2020-50-10', 1],
        ['2020-11-12', 1],
        ['2020-11-13', 1],
        ['2020-11-20', 1],
        ['2020-11-99', 1],
        ['2020-11-28', 1],
        ['2020-11-29', 1],
        ['2020-11-30', 1],
        ['2020-10-05', 1],
        ['2020-10-08', 1],
        ['2020-10-18', 0],
        ['2020-10-29', 0],
        ['2020-09-01', 0],
        ['2020-09-05', 0],
        ['2020-09-11', 0]
      ],
    }
  ];
  var user4habits = [];
  return user2habits;
}

/**
 * Takes the results of getRelevantDates and requestHabits to build a T3M chart for each of the habits logged for the current user.
*/
function renderHabitCharts() {
  // Render the relevant charts for the user's habit activity over the most recent 3 months.
  // Get the habit information for the current user.
  var habitList = requestHabits();
  // Get the needed date information to build the calendar.
  var dates = getRelevantDates(new Date());
  // Handle the case that the user has no habits yet.
  if (habitList.length == 0) {
    // Add a header specifying no habits yet added to the DOM.
    var header = document.createElement("H2");
    var headerText = document.createTextNode("No habits yet added.");
    header.appendChild(headerText);
    document.body.appendChild(header);
  }

  // Loop over the array of habits and add a header and chart.
  for (i = 0; i < habitList.length; i++) {
    var habitinfo = habitList[i];
    var habitname = habitinfo['name']
    // Create a header element with the name of the habit
    var header = document.createElement("H2");
    var headerText = document.createTextNode(habitname);
    header.appendChild(headerText);
    document.body.appendChild(header);
    // Create a div element in which to render that habit's chart and set the id to the name of the habit
    var div = document.createElement("div");
    div.setAttribute("id", habitname);
    document.body.appendChild(div);
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
      values: habitinfo['date_values']
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
