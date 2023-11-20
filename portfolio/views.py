from django.shortcuts import render
from .models import Stock, Option, Portfolio
import yfinance as yf
from datetime import datetime
from django.views import generic
#import json
 

def index(request):
    return render(request, 'portfolio/index.html', {})

def get_stock_data(request, pk):
    
    ticker = Stock.objects.get(pk=pk).symbol.upper()
    stock_ticker = yf.Ticker(ticker)
    now = datetime.now().strftime('%Y-%m-%d')
    ticker_history = stock_ticker.history(period='1d', interval='1m')
    price = ticker_history['Close'].iloc[-1]
    context = {
        'ticker': ticker,
        'price': price,
    }
    # How do you add spy ticker to the template???
    return render(request, 'portfolio/stock_detail.html', context=context)


def get_option_data(request, symbol):
    
    return render(request, 'portfolio/options.html', {})



class StockListView(generic.ListView):
    model = Stock
    context_object_name = 'stock_list'
    template_name = 'portfolio/stocks.html'