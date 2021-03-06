import datetime
import os
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import requests
import finnhub
from .forms import StockTickerForm, SignUpForm, LoginForm
from django.contrib.auth.models import User
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('.env'))

#############################################################################################

# Configure API key for finnhub API
configuration = finnhub.Configuration(
    api_key={
        'token': os.environ['DjangoStockMarketAppFinnhubAPIKEY']
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

    if request.user.is_authenticated:
        context["Username"] = request.user

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

        year1 = '{:02d}'.format(now.year - 1)
        year_before = '{:02d}'.format(now.month - 12)
        year_month_day1 = '{}-{}-{}'.format(year1, year_before, day)

        # Getting news from 1 year prior to now
        company_news = finnhub_client.company_news(stock_ticker, _from=year_month_day1, to=year_month_day2)

        context['company_news'] = company_news
        context['basic_financials'] = data
        context['Searchform'] = Searchform

    return render(request, 'Stocks/StockView.html', context)


##################################################################################################################

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
                # Fetching form data
                email = signUpForm.cleaned_data['email']
                username = signUpForm.cleaned_data['username']
                password = signUpForm.cleaned_data['password']

                if User.objects.filter(username=signUpForm.cleaned_data['username']):
                    messages.add_message(request, messages.ERROR, 'Username already taken!')
                    context["SignUpform"] = signUpForm
                    context["Searchform"] = StockTickerForm()
                    return render(request, 'Stocks/SignUpView.html', context)

                else:
                    # Create a new user from Member model object and save it to the database
                    member = User.objects.create_user(email=email, username=username, password=password)
                    member.save()

                    login(request, member)  # login the created user and redirect

                    return HttpResponseRedirect(reverse('stock_market:home'))

    else:

        context["SignUpform"] = SignUpForm()
        context["Searchform"] = StockTickerForm()

        return render(request, 'Stocks/SignUpView.html', context)


###################################################################################################################

def login_view(request):
    context = {}

    if request.method == 'GET':
        loginform = LoginForm()
        searchform = StockTickerForm()
        context['LoginForm'] = loginform
        context['Searchform'] = searchform
        return render(request, 'Stocks/LoginView.html', context)

    elif request.method == 'POST':

        # If the user searches for a stock ticker (even though they shouldn't)
        if "SearchButtonForm" in request.POST:
            Searchform = StockTickerForm(request.POST)

            if Searchform.is_valid():
                uppercase_ticker = Searchform.cleaned_data['ticker'].upper()
                return HttpResponseRedirect(reverse('stock_market:stock_view_url', args=[uppercase_ticker]))

        else:

            loginform = LoginForm(request.POST)

            if loginform.is_valid():

                username1 = request.POST['username']
                password1 = request.POST['password']

                # Validate user credentials
                user = authenticate(request, username=username1, password=password1)

                if user is not None:
                    login(request, user)
                    # Redirect to home page
                    return HttpResponseRedirect(reverse('stock_market:home'))

                else:
                    # Display an error message
                    messages.add_message(request, messages.ERROR, "Invalid credentials!")
                    context['LoginForm'] = loginform
                    searchform = StockTickerForm()
                    context['Searchform'] = searchform
                    return render(request, 'Stocks/LoginView.html', context)


################################################################################################################

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('stock_market:home'))
