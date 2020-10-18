function renderChart(data, labels) {
    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'This week',
                data: data,
            }]
        },
    });
}


window.onload = function() {
  setUpChart();
};

function setUpChart() {
  
  data = [20000, 14000, 12000, 15000, 18000, 19000, 22000];
  labels =  ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
  renderChart(data, labels);
}


$("#renderBtn").click(
    function () {
        data = [20000, 14000, 12000, 15000, 18000, 19000, 22000];
        labels =  ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
        renderChart(data, labels);
    }
);
