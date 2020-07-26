const symbol1 = document.getElementById('title').innerHTML;
const APIKey1 = "bs5qbcfrh5rajuf8m9ig";
const url1 = `https://finnhub.io/api/v1/stock/price-target?symbol=${symbol1}&token=${APIKey1}`;

var lastUpdated = "";
var price_Targets = [];

fetch(url1)
    .then( function(response1){

        // Convert response object to json() format
        return response1.json();

    })
    .then( function(data1) {

        lastUpdated = data1['lastUpdated'];
        price_Targets[0] = data1['targetHigh'];
        price_Targets[1] = data1['targetLow'];
        price_Targets[2] = data1['targetMean'];
        price_Targets[3] = data1['targetMedian'];

    })


var ctx = document.getElementById('PriceTargets').getContext('2d');

var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['Target High', 'Target Low', 'Target Mean', 'Target Median'],
        datasets: [{
            label: 'Price Estimates',
            backgroundColor: 'rgb(4,113,24)',
            borderColor: 'rgb(4,113,24)',
            data: price_Targets,
        },
        ]
    },

    // Configuration options go here
    options: {
        title:{
            display: true,
            position: 'top',
            text: 'Price Targets',
            fontStyle: 'bold',
            responsive: true,
        }

    }
});