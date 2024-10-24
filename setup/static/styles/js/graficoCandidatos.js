const mesesCandidatos = JSON.parse(document.getElementById('candidatosChart').getAttribute('data-meses'));
const totalCandidatos = JSON.parse(document.getElementById('candidatosChart').getAttribute('data-total'));

const ctx = document.getElementById('candidatosChart').getContext('2d');
const candidatosChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: mesesCandidatos,
        datasets: [{
            label: 'Total de Candidatos',
            data: totalCandidatos,
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            borderColor: 'rgba(153, 102, 255, 1)',
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
