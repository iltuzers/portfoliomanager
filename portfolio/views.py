from django.shortcuts import render
from .models import Stock, Option, Portfolio
import yfinance as yf
from datetime import datetime
import pandas as pd
from django.views import generic
from .utils import option_greeks, all_options
from django.contrib.auth.mixins import LoginRequiredMixin
#import json
 

def index(request):
    return render(request, 'portfolio/index.html', {})


def get_stock_data(request, pk):
    
    ticker = Stock.objects.get(pk=pk).symbol.upper()
    
    options = option_greeks(ticker)
    calls = options.loc[options.option_type == 'c', ['contractSymbol', 'expiration_date', 'dte', 'strike', 'volume', 'openInterest',  'IV', 'delta', 'gamma', 'theta', 'vega']]
    puts = options.loc[options.option_type == 'p', ['contractSymbol', 'expiration_date', 'dte', 'strike', 'volume', 'openInterest', 'IV', 'delta', 'gamma', 'theta', 'vega']]
    calls = calls.values.tolist()
    puts = puts.values.tolist()
    context = {
        'ticker': ticker,
        'calls': calls,
        'puts': puts,
        
    }
    return render(request, 'portfolio/stock_detail.html', context=context)


def get_all_options(request):
    ticker_queryset = Stock.objects.values('symbol')
    tickers = []
    for ticker_query in ticker_queryset:
        tickers.append(ticker_query['symbol'])
    options_df = all_options(tickers)
    options_df = options_df.loc[:, ['underlying', 'option_type', 'contractSymbol', 'expiration_date', 'dte', 'strike', 'volume', 'openInterest',  'IV', 'delta', 'gamma', 'theta', 'vega' ]]
    options_df = options_df.values.tolist()
    context = {
        'tickers': tickers,
        'options': options_df
    }
    return render(request, 'portfolio/options.html', context=context)



class StockListView(generic.ListView):
    model = Stock
    context_object_name = 'stock_list'
    template_name = 'portfolio/stocks.html'


class PortfolioListView(LoginRequiredMixin, generic.ListView):
    model = Portfolio
    template_name = 'portfolio/portfolio_list_current_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Portfolio.objects.filter(owner=self.request.user)













