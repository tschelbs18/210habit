test('adds 1 + 2 to equal 3', () => {
  var x = 3;
  expect(x).toBe(3);
});

/*
Notes:
Order doesn't matter for the dates, but value does for the opacity of the color.
- Should confirm that only 1s or 0s are coming into the values. Maybe build some logic to handle non-binary date_values
- T30D view for multiple months?
*/
// Single habit, all in one month
// var user1habits = [
//   {
//     'name': 'Running',
//     'date_values': [
//       ['2020-11-01', 1],
//       ['2020-11-02', 1],
//       ['2020-11-05', 1],
//       ['2020-11-08', 1],
//       ['2020-11-09', 1],
//       ['2020-11-14', 1],
//       ['2020-11-16', 1],
//       ['2020-11-30', 1],
//       ['2020-11-18', 1],
//       ['2020-11-29', 1],
//     ],
//   }
// ];
// // Multiple Habits with different date ranges and no data
// var user2habits = [
//   {
//     'name': 'Running',
//     'date_values': [
//       ['2020-10-01', 1],
//       ['2020-10-02', 1],
//       ['2020-10-05', 1],
//       ['2020-11-08', 1],
//       ['2020-11-18', 1],
//       ['2020-11-29', 1],
//     ],
//   },
//   {
//     'name': 'Reading',
//     'date_values': [
//       ['2020-09-01', 1],
//       ['2020-09-09', 1],
//       ['2020-11-25', 1],
//       ['2020-10-11', 1],
//       ['2020-10-14', 1],
//       ['2020-10-17', 1],
//     ],
//   },
//   {
//     'name': 'Meditating',
//     'date_values': [
//       ['2020-11-01', 1],
//       ['2020-11-02', 1],
//       ['2020-11-05', 1],
//       ['2020-11-08', 1],
//       ['2020-09-18', 1],
//       ['2020-10-29', 1],
//     ]
//   },
//   {
//     'name': 'Napping',
//     'date_values': [
//     ]
//   }
// ];
// // Illogical inputs
// var user3habits = [
//   {
//     'name': 'Running',
//     'date_values': [
//       ['xxxx-11-02', 1],
//       ['2020-11-09', 1],
//       ['2020-50-10', 1],
//       ['2020-11-12', 1],
//       ['2020-11-13', 1],
//       ['2020-11-20', 1],
//       ['2020-11-99', 1],
//       ['2020-11-28', 1],
//       ['2020-11-29', 1],
//       ['2020-11-30', 1],
//       ['2020-10-05', 1],
//       ['2020-10-08', 1],
//       ['2020-10-18', 0],
//       ['2020-10-29', 0],
//       ['2020-09-01', 0],
//       ['2020-09-05', 0],
//       ['2020-09-11', 0]
//     ],
//   }
// ];
// var user4habits = [];
// return user2habits;
