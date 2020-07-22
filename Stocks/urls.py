from django.urls import path
from Stocks import views

app_name = "stock_market"

urlpatterns = [

    path('', views.home_view, name='home'),
    path('stock/<str:stock_ticker>/', views.stock_view, name='stock_view_url'),

]
