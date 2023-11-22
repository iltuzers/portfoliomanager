import pandas as pd
import yfinance as yf
from datetime import datetime, date, timedelta
from py_vollib_vectorized.api import price_dataframe



def option_greeks(ticker, underlying_price, dividend_per_day, riskfree_rate=0.054, min_dte=22, max_dte=50):
    ticker_obj = yf.Ticker(ticker)
    expirations = ticker_obj.options
    puts_df = pd.DataFrame(columns=['expiration_date', 'contractSymbol', 'strike', 'bid', 'ask', 'volume', 'openInterest'])
    calls_df = pd.DataFrame(columns=['expiration_date', 'contractSymbol', 'strike', 'bid', 'ask', 'volume', 'openInterest'])
    for expiration in expirations:
        exp_date = datetime.strptime(expiration, "%Y-%m-%d").date()
        if min_dte <= (exp_date - datetime.now().date()).days <= max_dte:
        
            puts = ticker_obj.option_chain(expiration).puts
            calls = ticker_obj.option_chain(expiration).calls
            puts = puts.loc[:, ['contractSymbol', 'strike', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest', 'impliedVolatility']]
            puts = puts.assign(expiration_date=exp_date)
            calls = calls.loc[:, ['contractSymbol', 'strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'impliedVolatility']]
            calls = calls.assign(expiration_date=exp_date)
            puts_df = pd.concat([puts_df, puts], ignore_index=True)
            calls_df = pd.concat([calls_df, calls], ignore_index=True)

    puts_df['price'] = (puts_df['bid'] + puts_df['ask']) / 2
    puts_df.loc[puts_df['price'] == 0,  'price'] = puts_df.loc[puts_df['price'] == 0, 'lastPrice']  # bid-ask = 0 is mostly wrong in YF.
    calls_df['price'] = (calls_df['bid'] + calls_df['ask']) / 2
    calls_df.loc[calls_df['price'] == 0, 'price'] = calls_df.loc[calls_df['price'] == 0, 'lastPrice']
    puts_df.drop(['bid', 'ask', 'lastPrice'], axis=1, inplace=True)
    calls_df.drop(['bid', 'ask', 'lastPrice'], axis=1, inplace=True)

    # In order to use py_vollib, we need following columns
    puts_df = puts_df.assign(option_type='p')
    puts_df = puts_df.assign(underlying_price=underlying_price)
    puts_df = puts_df.assign(riskfree_rate=riskfree_rate)
    
    calls_df = calls_df.assign(option_type='c')
    calls_df = calls_df.assign(underlying_price=underlying_price)
    calls_df = calls_df.assign(riskfree_rate=riskfree_rate)

    puts_df['tte'] = (puts_df['expiration_date'] - datetime.now().date()).apply(lambda dt: int(dt.days))
    calls_df['tte'] = (calls_df['expiration_date'] - datetime.now().date()).apply(lambda dt: int(dt.days))
    if dividend_per_day:
        puts_df['dividend_yield'] = dividend_per_day * puts_df['tte'] / puts_df['underlying_price']
        calls_df['dividend_yield'] = dividend_per_day * calls_df['tte'] / puts_df['underlying_price']
    puts_df['tte'] = puts_df['tte'] / 360 # annualized time to expiration (dte / 360)
    calls_df['tte'] = calls_df['tte'] / 360

    #puts_df['riskfree_rate'] = puts_df['riskfree_rate'] * puts_df['tte']
    #calls_df['riskfree_rate'] = calls_df['riskfree_rate'] * calls_df['tte']

    

    options_df = pd.concat([puts_df, calls_df], ignore_index=True)
    #options_df = options_df.loc[options_df['price'] > 0]
    #options_df = options_df.loc[options_df['openInterest'] > 0]
    price_dataframe(options_df, flag_col = 'option_type', underlying_price_col = 'underlying_price', strike_col='strike', annualized_tte_col='tte', 
                riskfree_rate_col='riskfree_rate', price_col='price', dividend_col='dividend_yield', model='black_scholes', inplace=True)
    return options_df
