  var ctx = document.getElementById("myChart").getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["Day 1", "Day 2", "Day 3","Day 4","Day 5"],
      datasets: [{
        label: 'distance traveled',
        data: [29.5, 30.7, 15.3, 30.2, 31.5],
        backgroundColor: [
          'rgba(0, 200, 132, 0.2)',
          'rgba(0, 200, 132, 0.2)',
          'rgba(255, 99, 132, 0.2)',
          'rgba(0, 200, 132, 0.2)',
          'rgba(0, 200, 132, 0.2)',
        ],
        borderColor: [
          'rgba(0,200,132,1)',
          'rgba(0,200,132,1)',
          'rgba(255,99,132,1)',
          'rgba(0,200,132,1)',
          'rgba(0,200,132,1)',
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      }
    }
  });
