const symbol2 = document.getElementById('title').innerHTML;
const APIKey2 = "bs5qbcfrh5rajuf8m9ig";
const url2 = `https://finnhub.io/api/v1/stock/candle?symbol=${symbol2}&resolution=1&from=1572651390&to=1572910590&token=${APIKey2}`;

var candles = []; //List of dictionaries

fetch(url2)
    .then( function(response2){

        // Convert response object to json() format
        return response2.json();

    })
    .then( function(data2) {

        for(let i = 0; i < data2['c'].length; i++){
        	let obj = {};
        	obj['time'] = timeConverter(data2['t'][i]);
			obj['open'] = data2['o'][i];
			obj['high'] = data2['h'][i];
			obj['low'] = data2['l'][i];
			obj['close'] = data2['c'][i];

        	candles.push(obj);
		}

        console.log('Candles: ', candles);

    })

	.then(function () {
		var chart = LightweightCharts.createChart(document.getElementById('Stock_Chart'), {
			width: 600,
			height: 300,
			layout: {
				backgroundColor: '#000000',
				textColor: 'rgba(255, 255, 255, 0.9)',
			},
			grid: {
				vertLines: {
					color: 'rgba(197, 203, 206, 0.5)',
				},
				horzLines: {
					color: 'rgba(197, 203, 206, 0.5)',
				},
			},
			crosshair: {
				mode: LightweightCharts.CrosshairMode.Normal,
			},
			rightPriceScale: {
				borderColor: 'rgba(197, 203, 206, 0.8)',
			},
			timeScale: {
				borderColor: 'rgba(197, 203, 206, 0.8)',
			},
		});

		var candleSeries = chart.addCandlestickSeries({
			upColor: 'rgba(255, 144, 0, 1)',
			downColor: '#000',
			borderDownColor: 'rgba(255, 144, 0, 1)',
			borderUpColor: 'rgba(255, 144, 0, 1)',
			wickDownColor: 'rgba(255, 144, 0, 1)',
			wickUpColor: 'rgba(255, 144, 0, 1)',
		});

		candleSeries.setData(candles);

	});
//===========================================================================================================
//Helper function to convert a date to a 'year-month-day' format
function timeConverter(UNIX_timestamp){
  var a = new Date(UNIX_timestamp * 1000);
  var year = a.getFullYear();
  var month = a.getMonth()+1;
  var date = a.getDate();
  return year + '-' + month + '-' + date;
}