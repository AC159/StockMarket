
const symbol = document.getElementById('title').innerHTML;
const APIKey = "bs5qbcfrh5rajuf8m9ig";
const url = `https://finnhub.io/api/v1/stock/recommendation?symbol=${symbol}&token=${APIKey}`;

var dates = [];
var strongBuy = [];
var buy = [];
var hold = [];
var sell = [];

fetch(url)
    .then( function(response){

        // Convert response object to json() format
        return response.json();

    })
    .then( function(data) {

        //Getting the year-month-day time in chronological order
        for(let i = 0; i < data.length; i++){
            dates[i] = data[data.length-1-i]['period'];
            strongBuy[i] = data[data.length-1-i]['strongBuy'];
            buy[i] = data[data.length-1-i]['buy'];
            hold[i] = data[data.length-1-i]['hold'];
            sell[i] = data[data.length-1-i]['sell'];
        }

    })


var ctx = document.getElementById('StockRecommendations').getContext('2d');

var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'bar',

    // The data for our dataset
    data: {
        labels: dates,
        datasets: [{
            label: 'Strong Buy',
            backgroundColor: 'rgb(4,113,24)',
            borderColor: 'rgb(4,113,24)',
            data: strongBuy,
        },
        {
            label: 'Buy',
            backgroundColor: 'rgb(26,213,75)',
            borderColor: 'rgb(26,213,75)',
            data: buy,
        },
        {
            label: 'Hold',
            backgroundColor: 'rgb(234,171,7)',
            borderColor: 'rgb(234,171,7)',
            data: hold,
        },
        {
            label: 'Sell',
            backgroundColor: 'rgb(234,7,15)',
            borderColor: 'rgb(234,7,15)',
            data: sell,
        }

        ]
    },

    // Configuration options go here
    options: {
        title:{
            display: true,
            position: 'top',
            text: 'Recommendation Trends',
            fontStyle: 'bold'
        }

    }
});