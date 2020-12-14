// Copied from progress.js
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

test('Get the desired date values', () => {
  var today = new Date();
  var dates = getRelevantDates(today);
  var date_keys = Object.keys(dates);
  expect(date_keys).toContain('year');
  expect(date_keys).toContain('startMonth');
  expect(date_keys).toContain('endMonth');
  expect(dates['startMonth']).toBeGreaterThanOrEqual(1);
  expect(dates['startMonth']).toBeLessThanOrEqual(12);
  expect(dates['endMonth']).toBeGreaterThanOrEqual(1);
  expect(dates['endMonth']).toBeLessThanOrEqual(12);
  expect(dates['year']).toHaveLength(4);
  expect(parseInt(dates['year'])).toBeGreaterThanOrEqual(2020);
});
