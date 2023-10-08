from flask_restx import Namespace, Resource
from flask import request, jsonify
from flask_restx import Resource, fields
from sqlalchemy.orm import sessionmaker
from models import TradeSignals
import pandas as pd
import numpy as np
import os
from os import listdir
from app import db
import json

signals_ns = Namespace('/trade', description='a namespace for trades')

signals_model = signals_ns.model(
    "Trade Signal", 
    {
        "portfolio_id": fields.Integer(),
        "time": fields.String(),
        "asset_price1": fields.Float(),
        "asset_price2": fields.Float(),
        "zscore": fields.Float(),
        "recommendation": fields.String()
    }
)

@signals_ns.route('/initiate')
class TradeResource(Resource):
    
    @signals_ns.marshal_with(signals_model)
    def post(self):
        """ Create a new entry for the trade databse """
        data = request.json
        portfolio_id = data['id']
        ticker1 = data['asset1']
        ticker2 = data['asset2']

        ticker1 = ticker1.replace('/', '')
        ticker2 = ticker2.replace('/', '')


        table_data = entry_point(ticker1, ticker2)

        Session = sessionmaker(bind=db.engine)
        session = Session()

        try:

            for _, row in table_data.iterrows():

                time = row['Time']
                asset_price1 = row[ticker1]
                asset_price2 = row[ticker2]
                zscore = row['Z-Score']
                recommendation = row['Recommendations']

                new_entry = TradeSignals(
                    time=time,
                    portfolio_id=portfolio_id,
                    asset_price1=asset_price1,
                    asset_price2=asset_price2,
                    zscore=zscore,
                    recommendation=recommendation
                )
                session.add(new_entry)

            session.commit()

            return {"message": f"{ticker1} {ticker2} data added successfully"}, 201
        
        except Exception as e:
            session.rollback()  # Rollback changes if an error occurs
            print(e)
            return {"message": "Error occurred while adding entry to the trade database."}, 500
        finally:
            session.close()
        
    
@signals_ns.route('/trades/<int:id>')
class TradeResource(Resource):

    def get(self, id):
        signals = TradeSignals.query.filter_by(portfolio_id=id).all()
        
        recommendation_data = []
        for signal in signals:
            signal_dict = {
                "portfolio_id": signal.portfolio_id,
                "time": signal.time,
                "recommendation": signal.recommendation
            }
            if signal.recommendation:
                recommendation_data.append(signal_dict)

        return recommendation_data, 200

    def delete(self, id):
        
        signals_to_delete = TradeSignals.query.filter_by(portfolio_id=id).all()
        
        if signals_to_delete:
            for signal in signals_to_delete:
                db.session.delete(signal)

            db.session.commit()
            return {"message": "signals deleted successfully"}, 200
        else:
            return {"message": "no signals found for the given portfolio_id"}, 404

# This function loads historical data to populate the trade signals table with
class LoadData:

    def load_hist_data(ticker1, ticker2):
        current_script_directory = os.path.dirname(os.path.abspath(__file__))
        directory = os.path.join(current_script_directory, "hist_backtest_data")
        
        file = f"{ticker1}_{ticker2}_hist_data.csv"

        for filename in listdir(directory):
            if filename == file:
                filepath = os.path.join(directory, filename)
                df = pd.read_csv(filepath)
                return df

# This function has the main functions of the recommendation algorithm                     
def entry_point(ticker1, ticker2):

    data = LoadData.load_hist_data(ticker1, ticker2)
    data = data.drop(columns=['Unnamed: 0'])

    signals = generate_signals(data)
    return signals

# This function has the trading rules for the recommendation algorithm
def generate_signals(df):
    
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
        
    
    """
    Initialize the strategy (trade variables). Define entry and exit thresholds.
    """
    long_entry_threshold = -2
    short_entry_threshold = 2
    exit_threshold = 0
    
    df['Recommendations'] = None

    """
    Generate trade signal and monitor active trades.
    """
    def process_long_trade_ticker1(ticker, price):
        return (f"Go long on {ticker} now! It's current price is: {price}")
        
    def process_long_trade_ticker2(ticker, price):
        return (f"Go long on {ticker} now! It's current price is: {price}")

    def process_short_trade_ticker1(ticker, price):
        return (f"Go short on {ticker} now! It's current price is: {price}")

    def process_short_trade_ticker2(ticker, price):
        return (f"Go short on {ticker} now! It's current price is: {price}")

    def process_exit_trade_ticker1(ticker, price):
        return (f"Exit the position for {ticker} now! It's current price is: {price}")
        
    def process_exit_trade_ticker2(ticker, price):
        return (f"Exit the position for {ticker} now! It's current price is: {price}")

    active_long = False
    active_short = False

    trade_recommendations_dict = {}

    for index, row in df.iterrows():
        
        row_recommendations = []

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
                    row_recommendations.append(process_long_trade_ticker1(ticker1, price1))
                    active_long = True
                else:
                    row_recommendations.append(process_short_trade_ticker1(ticker1, price1))
                    active_long = True
                if price2 > lookback_price2:
                    row_recommendations.append(process_long_trade_ticker2(ticker2, price2))
                    active_long = True
                else:
                    row_recommendations.append(process_short_trade_ticker2(ticker2, price2))
                    active_long = True

            elif current_zscore >= exit_threshold and active_long == True:
                row_recommendations.append(process_exit_trade_ticker1(ticker1, price1))
                row_recommendations.append(process_exit_trade_ticker2(ticker2, price2))
                active_long = False
                
            if current_zscore >= short_entry_threshold and active_short == False:
                if price1 < lookback_price1:
                    row_recommendations.append(process_short_trade_ticker1(ticker1, price1))
                    active_short = True
                else:
                    row_recommendations.append(process_long_trade_ticker1(ticker1, price1))
                    active_short = True
                if price2 < lookback_price2:
                    row_recommendations.append(process_short_trade_ticker2(ticker2, price2))
                    active_short = True
                else:
                    row_recommendations.append(process_long_trade_ticker2(ticker2, price2))
                    active_short = True
            elif current_zscore <= exit_threshold and active_short == True:
                row_recommendations.append(process_exit_trade_ticker1(ticker1, price1))
                row_recommendations.append(process_exit_trade_ticker2(ticker2, price2))
                active_short = False
        
        trade_recommendations_dict[index] = row_recommendations   

    df['Recommendations'] = [", ".join(trade_recommendations_dict[index]) for index in df.index]
    df = df.sort_index(ascending=False)
    return df