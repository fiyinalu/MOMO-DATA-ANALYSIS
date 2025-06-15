// For now, dummy data to test chart
const data = [
  { transaction_type: "Incoming Money", amount: 5000 },
  { transaction_type: "Payments", amount: 1500 },
  { transaction_type: "Payments", amount: 3000 },
  { transaction_type: "Withdrawals", amount: 20000 },
  { transaction_type: "Internet Bundle Purchase", amount: 2000 }
];

// Function to group total amount by transaction type
function groupData(data) {
  const result = {};
  data.forEach(item => {
    if (!result[item.transaction_type]) {
      result[item.transaction_type] = 0;
    }
    result[item.transaction_type] += item.amount;
  });
  return result;
}

function updateChart(chart, groupedData) {
  chart.data.labels = Object.keys(groupedData);
  chart.data.datasets[0].data = Object.values(groupedData);
  chart.update();
}

window.onload = function () {
  const ctx = document.getElementById('transactionChart').getContext('2d');
  const groupedData = groupData(data);

  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(groupedData),
      datasets: [{
        label: 'Total Amount (RWF)',
        data: Object.values(groupedData),
        backgroundColor: 'rgba(54, 162, 235, 0.6)'
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });

  // Filter dropdown logic
  const filter = document.getElementById('typeFilter');
  filter.addEventListener('change', () => {
    let filteredData = data;
    if (filter.value !== 'all') {
      filteredData = data.filter(d => d.transaction_type === filter.value);
    }
    const grouped = groupData(filteredData);
    updateChart(chart, grouped);
  });
};
