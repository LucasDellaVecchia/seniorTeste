document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/graficoVagas')
        .then(response => response.json())
        .then(data => {
            const meses = data.meses;
            const totalVagas = data.total_vagas;

            const ctx = document.getElementById('vagasChart').getContext('2d');
            const vagasChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: meses,
                    datasets: [{
                        label: 'Total de Vagas',
                        data: totalVagas,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Erro ao carregar os dados:', error));
});
