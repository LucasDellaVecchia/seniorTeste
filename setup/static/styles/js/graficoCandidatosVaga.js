const labels = JSON.parse(document.getElementById('candidatosVagaChart').getAttribute('data-labels'));
const data = JSON.parse(document.getElementById('candidatosVagaChart').getAttribute('data-data'));

const ctx = document.getElementById('candidatosVagaChart').getContext('2d');
const candidatosVagaChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Total de Candidatos por Mês',
            data: data,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: false
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
