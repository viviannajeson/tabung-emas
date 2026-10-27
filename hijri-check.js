// Check the app's Hijri calendar (MABIMS criteria) against official Malaysian dates.
//   node hijri-check.js
const fs = require('fs');
const src = fs.readFileSync(__dirname + '/app.html', 'utf8');
const start = src.indexOf('const HJ = (() => {'), end = src.indexOf('})();', start) + 5;
const HJ = new Function(src.slice(start, end) + '\nreturn HJ;')();

// [Hijri date, Gregorian date in Malaysia, label]; add new announcements here as they are made.
const known = [
  ['1443-10-01', '2022-05-02', 'Aidilfitri 1443'], ['1443-12-10', '2022-07-10', 'Aidiladha 1443'],
  ['1444-09-01', '2023-03-23', '1 Ramadan 1444'], ['1444-10-01', '2023-04-22', 'Aidilfitri 1444'],
  ['1444-12-10', '2023-06-29', 'Aidiladha 1444'], ['1445-01-01', '2023-07-19', 'Awal Muharram 1445'],
  ['1445-09-01', '2024-03-12', '1 Ramadan 1445'], ['1445-10-01', '2024-04-10', 'Aidilfitri 1445'],
  ['1445-12-10', '2024-06-17', 'Aidiladha 1445'], ['1446-01-01', '2024-07-07', 'Awal Muharram 1446'],
  ['1446-03-12', '2024-09-16', 'Maulidur Rasul 1446'], ['1446-09-01', '2025-03-02', '1 Ramadan 1446'],
  ['1446-10-01', '2025-03-31', 'Aidilfitri 1446'], ['1446-12-10', '2025-06-07', 'Aidiladha 1446'],
  ['1447-01-01', '2025-06-27', 'Awal Muharram 1447'], ['1447-03-12', '2025-09-05', 'Maulidur Rasul 1447'],
];
let bad = 0;
for (const [h, g, label] of known) {
  const [y, m, d] = h.split('-').map(Number), got = HJ.fromHijri(y, m, d);
  if (got !== g) bad++;
  console.log(got === g ? 'OK' : 'XX', label.padEnd(22), g, got === g ? '' : `(app: ${got})`);
}
console.log(bad ? `${bad} mismatch` : 'All dates match');
process.exit(bad ? 1 : 0);
