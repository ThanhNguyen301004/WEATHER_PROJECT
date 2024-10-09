<script>
    window.onload = function () {
        var ctx = document.getElementById('myChart').getContext('2d');

        var gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(255, 0, 0, 0.5)');
        gradient.addColorStop(1, 'rgba(0, 255, 0, 0.5)');

        var times = {{ times | safe }};
        var temperatures = {{ temperatures | safe }};

        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: times,
                datasets: [{
                    label: 'Temperature (°C)',
                    data: temperatures,
                    backgroundColor: gradient,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtTen: true
                    }
                }
            }
        });
    }; 
</script>