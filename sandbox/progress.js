//document.body.onload = renderHabitCharts;

function getRelevantDates() {
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
  var yyyy = today.getFullYear();
  if (mm == '01') {
    var startMonth = 1;
    var endMonth = 1;
  } else if (mm == '02') {
    var startMonth = 1;
    var endMonth = 2;
  } else {
    var startMonth = parseInt(mm) - 2;
    var endMonth = parseInt(mm);
  }
  var dates = {'year': String(yyyy),
    'startMonth': startMonth,
    'endMonth': endMonth,
  };
  return dates;
}


function requestHabits() {
  // var xhr = new XMLHttpRequest();
  // xhr.open('GET', 'https://api.CSE210habit.com/user/habits', true);
  /*
  Notes:
  Order doesn't matter for the dates, but value does for the opacity of the color.
  - Should confirm that only 1s or 0s are coming into the values. Maybe build some logic to handle non-binary date_values
  - T30D view for multiple months?
  */
  var user1habits = {
    'habit': {
      'name': 'Running',
      'date_values': [
        ['2020-12-01', 1],
        ['2020-12-02', 1],
        ['2020-12-05', 1],
        ['2020-12-08', 1],
        ['2020-12-09', 1],
        ['2020-12-14', 1],
        ['2020-12-16', 1],
        ['2020-12-30', 1],
        ['2020-12-18', 1],
        ['2020-12-29', 1],
      ],
    }
  };
  var user2habits = {
    'habit': {
      'name': 'Running',
      'date_values': [
        ['2018-12-01', 1],
        ['2018-12-02', 1],
        ['2018-12-05', 1],
        ['2018-12-08', 1],
        ['2018-12-18', 1],
        ['2018-12-29', 1],
      ],
    },
    'habit': {
      'name': 'Reading',
      'date_values': [
        ['2019-12-01', 1],
        ['2019-12-09', 1],
        ['2019-12-25', 1],
        ['2019-12-11', 1],
        ['2019-12-14', 1],
        ['2019-12-17', 1],
      ],
    },
    'habit': {
      'name': 'Meditating',
      'date_values': [
        ['2020-11-01', 1],
        ['2020-11-02', 1],
        ['2020-11-05', 1],
        ['2020-11-08', 1],
        ['2020-09-18', 1],
        ['2020-10-29', 1],
      ]
    }
  };
  // need to handle multiple years of data being shown
  var user3habits = {
    'habit': {
      'name': 'Running',
      'date_values': [
        ['2020-11-02', 1],
        ['2020-11-09', 1],
        ['2020-11-10', 1],
        ['2020-11-12', 1],
        ['2020-11-13', 1],
        ['2020-11-20', 1],
        ['2020-11-27', 1],
        ['2020-11-28', 1],
        ['2020-11-29', 1],
        ['2020-11-30', 1],
        ['2020-10-05', 1],
        ['2020-10-08', 1],
        ['2020-10-18', 1],
        ['2020-10-29', 1],
        ['2020-09-01', 1],
        ['2020-09-05', 1],
        ['2020-09-11', 1]
      ],
    }
  };
  var user4habits = {};
  return user3habits;
}

function renderHabitCharts() {
  var habits = requestHabits();
  var dates = getRelevantDates();
  for(var key in habits) {
    var habitinfo = habits[key];
    var habitname = habitinfo['name']
    var header = document.createElement("H2");
    var headerText = document.createTextNode(habitname);
    header.appendChild(headerText);
    document.body.appendChild(header);
    var div = document.createElement("div");
    div.setAttribute("id", habitname);
    document.body.appendChild(div);
    var myConfig = {
    // should find a way to add the habit name as a title at the top of each calendar
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
  zingchart.loadModules('calendar', function(){
    zingchart.render({
      id: habitname,
      data: myConfig,
      height: 250,
      width: '60%'
    });
  });
  }
}
