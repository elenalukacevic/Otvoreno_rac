// sigurno prenosenje parametara za filtriranje za download
function updateDownloadLinks(filter = '', column = 'all') {
  const csvLink = document.getElementById('downloadCsv');
  const jsonLink = document.getElementById('downloadJson');

  csvLink.href = `/api/download/csv?filter=${encodeURIComponent(filter)}&column=${encodeURIComponent(column)}`;
  jsonLink.href = `/api/download/json?filter=${encodeURIComponent(filter)}&column=${encodeURIComponent(column)}`;
}

// dinamicko mjenjanje parametara i azuriranje linkova
async function fetchData(filter = '', column = 'all') {
  const res = await fetch(`/api/masine?filter=${filter}&column=${column}`);
  const data = await res.json();
  renderTable(data.response);
  updateDownloadLinks(filter, column);
}

// dinamicki prikaz tablice
function renderTable(data) {
  const table = document.getElementById('dataTable');
  if (!data.length) {
    table.innerHTML = '<tr><td>Nema podataka</td></tr>';
    return;
  }

  const cols = Object.keys(data[0]);
  let html = '<tr>' + cols.map(c => `<th>${c}</th>`).join('') + '</tr>';
  html += data.map(row => '<tr>' + cols.map(c => `<td>${row[c]}</td>`).join('') + '</tr>').join('');
  table.innerHTML = html;
}

document.getElementById('filterForm').addEventListener('submit', e => {
  e.preventDefault();
  const text = document.getElementById('searchText').value;
  const col = document.getElementById('searchColumn').value;
  fetchData(text, col);
});

// dohvacanje podataka
fetchData();

