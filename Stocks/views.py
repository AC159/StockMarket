import datetime
from random import randint
import os
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
import urllib3
import json
import requests
import finnhub
from .forms import StockTickerForm, SignUpForm
from langdetect import detect
import bcrypt

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
    context = {
        "forex_news": finnhub_client.general_news('forex', min_id=0),
        "general_news": finnhub_client.general_news('general', min_id=0),
        "merger_news": finnhub_client.general_news('merger', min_id=0),
        "crypto_news": finnhub_client.general_news('crypto', min_id=0)
    }

    # If the form is filled (i.e. it is a POST request), verify the input and redirect, otherwise stay on the same page
    if request.method == 'POST':

        # Checking which button was clicked so we can know which form has been submitted. The button in the HTML
        # template that submits the form must have a 'name' and 'value' which represent a 'key'-'value' pair in the
        # request.POST dictionary

        if 'SearchButtonForm' in request.POST:
            Searchform = StockTickerForm(request.POST)  # Bind the form to data to be able to perform validation after

            if Searchform.is_valid():
                uppercase_ticker = Searchform.cleaned_data['ticker'].upper()
                return HttpResponseRedirect(reverse('stock_market:stock_view_url', args=[uppercase_ticker]))

    else:  # else it is a GET request
        Searchform = StockTickerForm()  # Empty search form
        context['Searchform'] = Searchform  # Add empty search form to context

    return render(request, 'Stocks/base.html', context)

#####################################################################################################################

def stock_view(request, stock_ticker):
    context = {
        'ticker': stock_ticker,
        'company_profile': finnhub_client.company_profile2(symbol=stock_ticker),
        'quote': finnhub_client.quote(stock_ticker),
    }

    # If the form is filled (i.e. it is a POST request), verify the input and redirect, otherwise stay on the same page
    if request.method == 'POST':

        if 'SearchButtonForm' in request.POST:
            Searchform = StockTickerForm(request.POST)  # Bind the form to data to be able to perform validation after

            if Searchform.is_valid():
                uppercase_ticker = Searchform.cleaned_data['ticker'].upper()
                return HttpResponseRedirect(reverse('stock_market:stock_view_url', args=[uppercase_ticker]))

    else:  # else it is a GET request
        Searchform = StockTickerForm()  # Empty search form

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

            try:
                headline_number = randint(0, len(news) - 1)  # Generate random news number to pick from
            except ValueError:
                # There are no headlines
                break

            if headline_number not in headlines_chosen:
                # If the summary is empty or if the language is not english, then skip this headline
                if news[headline_number].summary == "" or detect(news[headline_number].headline) != 'en':
                    continue
                else:
                    headlines_chosen.append(
                        headline_number)  # Append the headline number to the list so we don't use it again
                    company_news.append(news[headline_number])
                    x += 1

            if count > 1000:
                break  # Take the news we have and display them (in order not to loop forever)

            count += 1

        context['company_news'] = company_news
        context['basic_financials'] = data
        context['Searchform'] = Searchform

    return render(request, 'Stocks/StockView.html', context)


def sign_up_view(request):
    context = {}

    if request.method == 'POST':
        if "SearchButtonForm" in request.POST:
            Searchform = StockTickerForm(request.POST)

            if Searchform.is_valid():
                uppercase_ticker = Searchform.cleaned_data['ticker'].upper()
                return HttpResponseRedirect(reverse('stock_market:stock_view_url', args=[uppercase_ticker]))

        elif "SignUpButton" in request.POST:
            signUpForm = SignUpForm(request.POST)

            if signUpForm.is_valid():
                # Create a session for the user


                return HttpResponseRedirect(reverse('stock_market:home'))

    else:

        context["SignUpform"] = SignUpForm()
        context["Searchform"] = StockTickerForm()

        return render(request, 'Stocks/SignUpView.html', context)


def login_view(request):
    context = {}

    return render(request, 'Stocks/LoginView.html', context)


def logout_view(request):
    pass