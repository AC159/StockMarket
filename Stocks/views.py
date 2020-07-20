import datetime
from random import randint
import os
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
import urllib3
import json
import requests
import finnhub
from .forms import StockTickerForm
from langdetect import detect

#############################################################################################

# Configure API key for finnhub API
configuration = finnhub.Configuration(
    api_key={
        'token': os.environ.get('DjangoStockMarketAppFinnhubAPIKEY')
    }
)
finnhub_client = finnhub.DefaultApi(finnhub.ApiClient(configuration))


#############################################################################################

# Create your views here.

def home_view(request):

    # If the form is filled (i.e. it is a POST request), verify the input and redirect, otherwise stay on the same page
    if request.method == 'POST':
        form = StockTickerForm(request.POST)  # Bind the form to data to be able to perform validation after
        context = {
            "forex_news": finnhub_client.general_news('forex', min_id=0),
            "general_news": finnhub_client.general_news('general', min_id=0),
            "merger_news": finnhub_client.general_news('merger', min_id=0),
            "form": form
        }
        if form.is_valid():
            uppercase_ticker = form.cleaned_data['ticker'].upper()
            return HttpResponseRedirect(reverse('stock_market:stock_view_url', args=[uppercase_ticker]))

    else:  # else it is a GET request
        form = StockTickerForm()  # Empty form
        context = {
            "crypto_news": finnhub_client.general_news('crypto', min_id=0),
            "general_news": finnhub_client.general_news('general', min_id=0),
            "merger_news": finnhub_client.general_news('merger', min_id=0),
            "form": form
        }

    return render(request, 'Stocks/base.html', context)


def stock_view(request, stock_ticker):

    # If the form is filled (i.e. it is a POST request), verify the input and redirect, otherwise stay on the same page
    if request.method == 'POST':
        form = StockTickerForm(request.POST)  # Bind the form to data to be able to perform validation after
        context = {
            'ticker': stock_ticker,
            'form': form
        }
        if form.is_valid():
            uppercase_ticker = form.cleaned_data['ticker'].upper()
            return HttpResponseRedirect(reverse('stock_market:stock_view_url', args=[uppercase_ticker]))

    else:  # else it is a GET request
        form = StockTickerForm()  # Empty form

        # Getting company basics financials
        r = requests.get(
            f"https://finnhub.io/api/v1/stock/metric?symbol={stock_ticker}&metric=all&token={os.environ.get('DjangoStockMarketAppFinnhubAPIKEY')}")
        data = r.json()

        # Dates for company news
        now = datetime.datetime.now()
        year = '{:02d}'.format(now.year)
        month = '{:02d}'.format(now.month)
        day = '{:02d}'.format(now.day)
        year_month_day2 = '{}-{}-{}'.format(year, month, day)

        month_before = '{:02d}'.format(now.month - 1)
        year_month_day1 = '{}-{}-{}'.format(year, month_before, day)

        # Getting news from 1 month prior to now
        news = finnhub_client.company_news(stock_ticker, _from=year_month_day1, to=year_month_day2)
        company_news = []
        headlines_chosen = []

        # Choosing 10 random headlines from the list
        count, x = 0, 0
        while x < 10:
            headline_number = randint(0, len(news) - 1)  # Generate random news number to pick from

            if headline_number not in headlines_chosen:
                # If the summary is empty or if the language is not english, then skip this headline
                if news[headline_number].summary == " " or detect(news[headline_number].headline) != 'en':
                    continue
                else:
                    headlines_chosen.append(headline_number)  # Append the headline number to the list so we don't use it again
                    company_news.append(news[headline_number])
                    x += 1

            if count > 1000:
                break  # Take the news we have and display them (in order not to loop forever)

            count += 1

        context = {
            'ticker': stock_ticker,
            'form': form,
            'company_profile': finnhub_client.company_profile2(symbol=stock_ticker),
            'quote': finnhub_client.quote(stock_ticker),
            'company_news': company_news,
            'basic_financials': data
        }

    return render(request, 'Stocks/StockView.html', context)
