**Getting Started with the Django Stock Market App**

1) Set up an environment variable for the SECRET_KEY and set its name to the
following: "DjangoStockMarketAppSecretKey"

2) Get an API key from Finnhub (https://finnhub.io/)

3) Set up an environment variable for Finnhub's API key and set its name to the
following: "DjangoStockMarketAppFinnhubAPIKEY"

4) In your terminal, install django widget tweaks with the following command:
pip install django-widget-tweaks

5) Go to the Recommendations_Chart.js file and set the 'APIKey' constant to your own API key.

6) Include a .env file at the root folder of the project and include:
    DATABASE_NAME=stockmarketapp
    DATABASE_USER=postgres
    DATABASE_PASSWORD=postgres
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    
    DjangoStockMarketAppFinnhubAPIKEY=<your api key>
    DjangoStockMarketAppSecretKey=<your secret key>