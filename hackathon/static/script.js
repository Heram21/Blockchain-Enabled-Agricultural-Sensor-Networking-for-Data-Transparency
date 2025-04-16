// Function to initialize and update the chart
function initializeChart() {
    const ctx = document.getElementById('sensorChart').getContext('2d');

    // Initialize the chart with empty data
    const sensorChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Timestamps will go here
            datasets: [
                {
                    label: 'Temperature (Â°C)',
                    data: [], // Temperature values will go here
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderWidth: 2,
                    fill: true,
                },
                {
                    label: 'Humidity (%)',
                    data: [], // Humidity values will go here
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderWidth: 2,
                    fill: true,
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                },
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Timestamp',
                    },
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Value',
                    },
                    beginAtZero: false,
                },
            },
        },
    });

    return sensorChart;
}

// Function to fetch data and update the chart
function updateChart(sensorChart) {
    fetch('/data') // Fetch data from Flask backend
        .then(response => response.json())
        .then(data => {
            // Extract timestamps and sensor values
            const timestamps = data.map(entry => entry.timestamp);
            const temperatures = data.map(entry => parseFloat(entry.temperature) || null);
            const humidities = data.map(entry => parseFloat(entry.humidity) || null);

            // Update the chart data
            sensorChart.data.labels = timestamps; // Update timestamps
            sensorChart.data.datasets[0].data = temperatures; // Update temperature data
            sensorChart.data.datasets[1].data = humidities; // Update humidity data

            // Re-render the chart
            sensorChart.update();
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Entry point: Initialize the chart and set up periodic updates
document.addEventListener("DOMContentLoaded", function () {
    // Initialize the chart
    const sensorChart = initializeChart();

    // Fetch data immediately on page load
    updateChart(sensorChart);

    // Set up periodic updates (every 60 seconds)
    setInterval(() => updateChart(sensorChart), 60000);
});
