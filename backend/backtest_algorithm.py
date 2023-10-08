from flask_restx import Namespace, Resource
from flask import jsonify
import os
from os import listdir
from os.path import join
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from itertools import combinations
from binance.client import Client
from binance.exceptions import BinanceAPIException
from statsmodels.tsa.vector_ar.vecm import *
import quantstats as qs

backtest_ns = Namespace('backtest', description="A namespace for the backtest software")

@backtest_ns.route('/initiate')
class BacktestResource(Resource):

    def get(self):
        backtest = entry_point()
        return backtest
    
    def post(self):

        global cancel_analysis

        cancel_analysis = True

        json_response = 'Program cancelled by user'
        return jsonify(json_response)
    

# This class gathers real-time data for the backtest algorithms 
class RealtimeData:
    
    def get_realtime_data(ticker1, ticker2):

        time_now = datetime.now()
        days =  timedelta(days=30)
        hist_time = str(time_now - days)

        api_key = "XNtTbIxyiAv3kKppkET8uuzRGLqa1DmNxh7mCDosiY41vkQu87nKzaTVfRgHS5C6"
        secret_key = "cfdm7bPCwJ5fzZZ15rqKcLjFFMz7Q9nk4rEpXwBeTo0LMFEQA2CLQoZh4zZI40Nv"
        interval = Client.KLINE_INTERVAL_1MINUTE
        # Create a Binance API client
        client = Client(api_key, secret_key)

        try: 
            data1 = client.get_historical_klines(symbol=ticker1, interval=interval, start_str=hist_time)
            data2 = client.get_historical_klines(symbol=ticker2, interval=interval, start_str=hist_time)

            timestamps = []
            close_prices1 = []
            close_prices2 = []

            for i in data1:
                close_prices1.append(float(i[4]))  # Index 4 corresponds to the close price
                undo_unix = datetime.fromtimestamp(i[0] / 1000)
                timestamps.append(undo_unix)
            
            for i in data2:
                close_prices2.append(float(i[4])) 

            if len(close_prices2) > len(close_prices1):
                close_prices2 = close_prices2[:len(close_prices1)]

        except BinanceAPIException as e:
            print("An API error occurred:")
            print(f"Error code: {e.code}")
            print(f"Error message: {e.message}")

        try:
            time = 'Time'
            df = pd.DataFrame({time: timestamps, ticker1: close_prices1, ticker2: close_prices2})
            return df
        except ValueError:
            print(f"error processing {ticker1} - {ticker2} data")

# This class loads data to run historical backtests
class LoadData:

    def load_hist_data():

        current_script_directory = os.path.dirname(os.path.abspath(__file__))
        directory = os.path.join(current_script_directory, "hist_backtest_data")
        paths = []

        for filename in listdir(directory):
            path = join(directory, filename)
            df = pd.read_csv(path)
            paths.append(df)

        return paths

# This class creates trade objects
class Trade:
    def __init__(self, ticker, price, order_type):
        self.ticker = ticker
        self.price = price
        self.order_type = order_type
    
    @classmethod
    def long(cls, ticker, price):
        return cls(ticker, price, 'long')

    @classmethod
    def short(cls, ticker, price):
        return cls(ticker, price, 'short')

    @classmethod
    def exit(cls, ticker, price):
        return cls(ticker, price, 'exit')

# This function carries out the main logic for the backtest algorithm. 
def entry_point():
    global cancel_analysis

    cancel_analysis = False

    # hist_ticker1_list = ['BCHUSDT','BCHUSDT','BCHUSDT','BCHUSDT','BCHUSDT','BNBUSDT','BNBUSDT','BNBUSDT','BNBUSDT','BTCUSDT','BTCUSDT','BTCUSDT','BTCUSDT','BTCUSDT','BTCUSDT','BTCUSDT','BTCUSDT','BTCUSDT','BUSDUSDT','BUSDUSDT','BUSDUSDT','ETHUSDT','ETHUSDT','ETHUSDT','ETHUSDT','ETHUSDT','ETHUSDT','FILUSDT','FILUSDT','LTCUSDT','LTCUSDT','LTCUSDT','LTCUSDT','LTCUSDT','LTCUSDT','LTCUSDT','MDTUSDT','XVGUSDT','XVGUSDT','XVGUSDT','XVGUSDT','XVGUSDT','XVGUSDT','XVGUSDT','XVGUSDT']
    # hist_ticker2_list = ['BNBUSDT','BUSDUSDT','COMPUSDT','FILUSDT','MDTUSDT','BUSDUSDT','COMPUSDT','FILUSDT','MDTUSDT','BCHUSDT','BNBUSDT','BUSDUSDT','COMPUSDT','ETHUSDT','FILUSDT','LTCUSDT','MDTUSDT','XVGUSDT','COMPUSDT','FILUSDT','MDTUSDT','BCHUSDT','BNBUSDT','BUSDUSDT','COMPUSDT','FILUSDT','MDTUSDT','COMPUSDT','MDTUSDT','BCHUSDT','BNBUSDT','BUSDUSDT','COMPUSDT','ETHUSDT','FILUSDT','MDTUSDT','COMPUSDT','BCHUSDT','BNBUSDT','BUSDUSDT','COMPUSDT','ETHUSDT','FILUSDT','LTCUSDT','MDTUSDT']
    # hist_output_df = pd.DataFrame(columns=['Ticker1', 'Ticker2', 'Sharpe Ratio', 'Cumulative Returns'])
    # hist_output_df['Ticker1'] = hist_ticker1_list
    # hist_output_df['Ticker2'] = hist_ticker2_list

    # data = LoadData.load_hist_data()
    # for i in data:
    #     data_df = i.iloc[:, 1:]

    #     if cancel_analysis == False:
                
    #         if cointegration_test(data_df):

    #             ticker1, ticker2, sharpe_ratio, cum_returns = backtest(data_df)
                        
    #             for index, row in hist_output_df.iterrows():
    #                 if row['Ticker1'] == ticker1 and row['Ticker2'] == ticker2:
    #                     hist_output_df.loc[index, 'Sharpe Ratio'] = sharpe_ratio
    #                     hist_output_df.loc[index, 'Cumulative Returns'] = cum_returns

    #             print(f'{ticker1} - {ticker2} added to df')
                    
    #     else:
    #         print("break")
    #         break
                
    # hist_output_df.dropna(inplace=True)
    # hist_output_df['Sharpe Ratio'] = hist_output_df['Sharpe Ratio'].astype(float)
    # hist_output_df['Cumulative Returns'] = hist_output_df['Cumulative Returns'].astype(float)
    # hist_output_df['Sharpe Ratio'] = hist_output_df['Sharpe Ratio'].round(2)
    # hist_output_df['Cumulative Returns'] = hist_output_df['Cumulative Returns'].round(2)
    # hist_output_df.sort_values('Sharpe Ratio', ascending=False, inplace=True)
    # hist_output_df['Ticker1'] = hist_output_df['Ticker1'].str.replace('USDT', '') + '/USDT'
    # hist_output_df['Ticker2'] = hist_output_df['Ticker2'].str.replace('USDT', '') + '/USDT'
    # json_response = hist_output_df.to_json(orient='records', lines=True)
    # return jsonify(json_response)

    tickers = find_pairs()

    tickers['Sharpe Ratio'] = None
    tickers['Cumulative Returns'] = None

    for index, row in tickers.iterrows():

        if cancel_analysis == False:

            ticker1, ticker2 = row["Ticker1"], row["Ticker2"]
            data_df = RealtimeData.get_realtime_data(ticker1, ticker2)
                    
            if cointegration_test(data_df):
                            
                asset1, asset2, sharpe_ratio, cumulative_returns = backtest(data_df)
                        
                tickers.loc[index, 'Sharpe Ratio'] = sharpe_ratio
                tickers.loc[index, 'Cumulative Returns'] = cumulative_returns
                
        else:
            break
            
    tickers.dropna(inplace=True)
    tickers['Sharpe Ratio'] = tickers['Sharpe Ratio'].astype(float)
    tickers['Cumulative Returns'] = tickers['Cumulative Returns'].astype(float)
    tickers['Sharpe Ratio'] = tickers['Sharpe Ratio'].round(2)
    tickers['Cumulative Returns'] = tickers['Cumulative Returns'].round(2)
    tickers['Ticker1'] = tickers['Ticker1'].str.replace('USDT', '') + '/USDT'
    tickers['Ticker2'] = tickers['Ticker2'].str.replace('USDT', '') + '/USDT'
    tickers.sort_values('Sharpe Ratio', ascending=False, inplace=True)
        
    json_response = tickers.to_json(orient='records', lines=True)
    return jsonify(json_response)

# This function accepts a number of coins and finds all pair combinations. 
def find_pairs():

    api_key = "XNtTbIxyiAv3kKppkET8uuzRGLqa1DmNxh7mCDosiY41vkQu87nKzaTVfRgHS5C6"
    secret_key = "cfdm7bPCwJ5fzZZ15rqKcLjFFMz7Q9nk4rEpXwBeTo0LMFEQA2CLQoZh4zZI40Nv"
    # Create a Binance API client
    client = Client(api_key, secret_key)
    interval = Client.KLINE_INTERVAL_1MONTH
    tickers_obj = client.get_all_tickers()

    time_now = datetime.now()
    days =  timedelta(days=30)
    hist_time = str(time_now - days)

    ticker_info_dict = {}

    for ticker in tickers_obj:
        data = client.get_historical_klines(symbol=ticker['symbol'], interval=interval, start_str=hist_time)
        if data is not None and data:
            num_trades = float(data[0][8])
            if num_trades is not None:
                num_trades = float(num_trades)
            ticker_info_dict[ticker['symbol']] = num_trades
        else:
            ticker_info_dict[ticker['symbol']] = None 
            
    ticker_tuple = list(ticker_info_dict.items())
        
    df = pd.DataFrame(ticker_tuple, columns=['Ticker', 'Number of Trades'])
    df = df.sort_values('Number of Trades', ascending=False)
        
    check_col = df['Ticker'].astype(str).str[-4:]

    select_usdt = (check_col == 'USDT')
    updated_df = df[select_usdt]

    updated_df = updated_df[:10]
        
    ticker_combinations = list(combinations(updated_df['Ticker'], 2))

    df_combinations = pd.DataFrame(ticker_combinations, columns=['Ticker1', 'Ticker2'])
    
    return df_combinations

# This function performs cointegration tests                  
def cointegration_test(df):

    ticker1 = df.columns[1]
    ticker2 = df.columns[2]

    # removing the index for the cointegration test
    pair_df = df[[ticker1, ticker2]]

    # Run cointegration test on pair.
    coint_test = coint_johansen(pair_df, det_order=0, k_ar_diff=1)
    trace = coint_test.lr1[0] # Trace Stat for cointegration of order 1
    crit_vals = coint_test.cvm[0][1] # Critical Value at 95% CI
    
    if trace > crit_vals:
        return True

# This function backtests the data and gives predicted profits.  
def backtest(df):
    
    # Define the ticker1 and ticker2 variables
    ticker1 = df.columns[1]
    ticker2 = df.columns[2]

    # Define list to store calculations temporarily      
    spread_list = []
    zscore_list = []

    # Define the lookback period
    lookback_period = 60

    for _, row in df.iterrows():

        # Calculate the spread
        price1, price2 = row[ticker1], row[ticker2]
        spread = price1 - price2
        spread_list.append(spread)

            # Calculate the mean, standard deviation, and z-score
        if len(spread_list) >= lookback_period:
            # Calculate the moving average
            ma = np.mean(spread_list[-lookback_period:])
            # Calculate the moving standard deviation
            std = np.std(spread_list[-lookback_period:])
            # Calculate the Z-Score
            if std != 0:
                zscore = (spread - ma) / std
            else:
                zscore = np.nan  # Assign NaN or any other value to represent an invalid z-score
        else:
            zscore = np.nan  # Assign NaN or any other value when there are not enough data points for the lookback period

        zscore_list.append(zscore)
        
    zscore_df = pd.DataFrame(zscore_list, columns=["Z-Score"])
    df = pd.concat([df, zscore_df], axis=1)
        
    df['Wallet Balance'] = 0
    
    """
    Initialize the strategy (trade variables). Define entry and exit thresholds.
    """
    long_entry_threshold = -2
    short_entry_threshold = 2
    exit_threshold = 0
    trade_log = []

    """
    Generate trade signal and monitor active trades.
    """
    def process_long_trade_ticker1(ticker, price):
        long_trade = Trade.long(ticker, price)
        trade_log.append(long_trade)
        
    def process_long_trade_ticker2(ticker, price):
        long_trade = Trade.long(ticker, price)
        trade_log.append(long_trade)

    def process_short_trade_ticker1(ticker, price):
        short_trade = Trade.short(ticker, price)
        trade_log.append(short_trade)

    def process_short_trade_ticker2(ticker, price):
        short_trade = Trade.short(ticker, price)
        trade_log.append(short_trade)

    def process_exit_trade_ticker1(ticker, price):
        exit_trade = Trade.exit(ticker, price)
        trade_log.append(exit_trade)
        
    def process_exit_trade_ticker2(ticker, price):
        exit_trade = Trade.exit(ticker, price)
        trade_log.append(exit_trade)

    active_long = False
    active_short = False

    for index, row in df.iterrows():
        if index >= 3:
            lookback_row = df.loc[index - 3]

            price1, price2 = row[ticker1], row[ticker2]
            current_zscore = row["Z-Score"]
            lookback_price1 = lookback_row[ticker1]
            lookback_price2 = lookback_row[ticker2]

            """
            This logic defines entry and exit criteria for a trade
            """
            if current_zscore <= long_entry_threshold and active_long == False:
                if price1 > lookback_price1:
                    process_long_trade_ticker1(ticker1, price1)
                    active_long = True
                else:
                    process_short_trade_ticker1(ticker1, price1)
                    active_long = True
                if price2 > lookback_price2:
                    process_long_trade_ticker2(ticker2, price2)
                    active_long = True
                else:
                    process_short_trade_ticker2(ticker2, price2)
                    active_long = True

            elif current_zscore >= exit_threshold and active_long == True:
                process_exit_trade_ticker1(ticker1, price1)
                process_exit_trade_ticker2(ticker2, price2)
                active_long = False
                
            if current_zscore >= short_entry_threshold and active_short == False:
                if price1 < lookback_price1:
                    process_short_trade_ticker1(ticker1, price1)
                    active_short = True
                else:
                    process_long_trade_ticker1(ticker1, price1)
                    active_short = True
                if price2 < lookback_price2:
                    process_short_trade_ticker2(ticker2, price2)
                    active_short = True
                else:
                    process_long_trade_ticker2(ticker2, price2)
                    active_short = True
            elif current_zscore <= exit_threshold and active_short == True:
                process_exit_trade_ticker1(ticker1, price1)
                process_exit_trade_ticker2(ticker2, price2)
                active_short = False

        """
        This logic analyses the profitability of the strategy
        """
        """
        Define capital variables
        """
        capital = 1000
        wallet_balance = capital
        allocation_ratio = 0.5
        cap_allo_ticker1 = capital * allocation_ratio
        cap_allo_ticker2 = capital * allocation_ratio
        transaction_cost = 0.1

        for trade in range(len(trade_log) - 3):
            current_trade = trade_log[trade]
            second_trade = trade_log[trade + 1]
            third_trade = trade_log[trade + 2]
            fourth_trade = trade_log[trade + 3]
                
            if (
                current_trade.order_type == "long"
                and second_trade.order_type == "long"
                and third_trade.order_type == "exit"
                and fourth_trade.order_type == "exit"
            ):
                entry_price1 = current_trade.price
                entry_price2 = second_trade.price
                exit_price1 = third_trade.price
                exit_price2 = fourth_trade.price

                # Calculate position sizes when entering the trade
                num_units_ticker1 = (cap_allo_ticker1 * (1 - transaction_cost)) / entry_price1
                num_units_ticker2 = (cap_allo_ticker2 * (1 - transaction_cost))/ entry_price2

                # Calculate the profit of the long position
                ticker1_profit = (exit_price1 - entry_price1) * num_units_ticker1
                ticker1_profit_with_trans = ticker1_profit * (1 - transaction_cost)
                ticker2_profit = (exit_price2 - entry_price2) * num_units_ticker2
                ticker2_profit_with_trans = ticker2_profit * (1 - transaction_cost)
                total_trade_profit = ticker1_profit_with_trans + ticker2_profit_with_trans

                wallet_balance += total_trade_profit

            elif (
                current_trade.order_type == "long"
                and second_trade.order_type == "short"
                and third_trade.order_type == "exit"
                and fourth_trade.order_type == "exit"
            ):
                entry_price1 = current_trade.price
                entry_price2 = second_trade.price
                exit_price1 = third_trade.price
                exit_price2 = fourth_trade.price

                # Calculate position sizes when entering the trade
                num_units_ticker1 = (cap_allo_ticker1 * (1 - transaction_cost)) / entry_price1
                num_units_ticker2 = (cap_allo_ticker2 * (1 - transaction_cost))/ entry_price2

                # Calculate the profit of the long position
                ticker1_profit = (exit_price1 - entry_price1) * num_units_ticker1 
                ticker1_profit_with_trans = ticker1_profit * (1 - transaction_cost)
                ticker2_profit = (entry_price2 - exit_price2) * num_units_ticker2 
                ticker2_profit_with_trans = ticker2_profit * (1 - transaction_cost)
                total_trade_profit = ticker1_profit_with_trans + ticker2_profit_with_trans

                wallet_balance += total_trade_profit
                
            elif (
                current_trade.order_type == "short"
                and second_trade.order_type == "short"
                and third_trade.order_type == "exit"
                and fourth_trade.order_type == "exit"
            ):
                entry_price1 = current_trade.price
                entry_price2 = second_trade.price
                exit_price1 = third_trade.price
                exit_price2 = fourth_trade.price

                # Calculate position sizes when entering the trade
                num_units_ticker1 = (cap_allo_ticker1 * (1 - transaction_cost)) / entry_price1
                num_units_ticker2 = (cap_allo_ticker2 * (1 - transaction_cost))/ entry_price2

                # Calculate the profit of the long position
                ticker1_profit = (entry_price1 - exit_price1) * num_units_ticker1 
                ticker1_profit_with_trans = ticker1_profit * (1 - transaction_cost)
                ticker2_profit = (entry_price2 - exit_price2) * num_units_ticker2
                ticker2_profit_with_trans = ticker2_profit * (1 - transaction_cost)
                total_trade_profit = ticker1_profit_with_trans + ticker2_profit_with_trans

                wallet_balance += total_trade_profit
                
            elif (
                current_trade.order_type == "short"
                and second_trade.order_type == "long"
                and third_trade.order_type == "exit"
                and fourth_trade.order_type == "exit"
            ):
                entry_price1 = current_trade.price
                entry_price2 = second_trade.price
                exit_price1 = third_trade.price
                exit_price2 = fourth_trade.price

                # Calculate position sizes when entering the trade
                num_units_ticker1 = (cap_allo_ticker1 * (1 - transaction_cost)) / entry_price1
                num_units_ticker2 = (cap_allo_ticker2 * (1 - transaction_cost))/ entry_price2

                # Calculate the profit of the long position
                ticker1_profit = (entry_price1 - exit_price1) * num_units_ticker1
                ticker1_profit_with_trans = ticker1_profit * (1 - transaction_cost)
                ticker2_profit = (exit_price2 - entry_price2) * num_units_ticker2
                ticker2_profit_with_trans = ticker2_profit * (1 - transaction_cost)
                total_trade_profit = ticker1_profit_with_trans + ticker2_profit_with_trans

                wallet_balance += total_trade_profit
    
        df.loc[index, 'Wallet Balance'] = wallet_balance

    qs.extend_pandas()

    df['Time'] = pd.to_datetime(df['Time'])
    df.set_index('Time', inplace=True)
    df_30 = df.resample('D').first()
    df_30.reset_index(inplace=True)
            
    df_30['Daily Returns'] = (df_30['Wallet Balance'] - df_30['Wallet Balance'].shift(1)) / df_30['Wallet Balance'].shift(1)
            
    returns = df_30['Daily Returns']
    returns = pd.Series(returns)

    sharpe_ratio = qs.stats.sharpe(returns)

    initial_value = df_30['Wallet Balance'].iloc[0]
    final_value = df_30['Wallet Balance'].iloc[-1]
    diff = final_value - initial_value
    cumulative_returns = diff / initial_value * 100

    return ticker1, ticker2, sharpe_ratio, cumulative_returns
        