from flask_restx import Namespace, Resource
from flask_restx import Resource, fields
from models import Tickers
from flask_jwt_extended import jwt_required
from binance.client import Client
from app import db

ticker_table_ns = Namespace('tickers', description="A namespace for a table containing realtime price updates from Binance")

ticker_model = ticker_table_ns.model (
    "Tickers",
    {
        "symbol": fields.String(),
        "price": fields.Float(),
    }
)

@ticker_table_ns.route('/populate')
class TickerPopulation(Resource):

    def get(self):

        tickers = Tickers.query.all()

        ticker_data = []

        for ticker in tickers:
            ticker_dict = {
                "symbol": ticker.symbol,
                "price": ticker.price
            }
            ticker_data.append(ticker_dict)

        return ticker_data

    def post(self):

        api_key = "XNtTbIxyiAv3kKppkET8uuzRGLqa1DmNxh7mCDosiY41vkQu87nKzaTVfRgHS5C6"
        secret_key = "cfdm7bPCwJ5fzZZ15rqKcLjFFMz7Q9nk4rEpXwBeTo0LMFEQA2CLQoZh4zZI40Nv"
        # Create a Binance API client
        client = Client(api_key, secret_key)
        tickers = client.get_all_tickers()

        for ticker in tickers: 
            symbol = ticker['symbol']
            price = float(ticker['price'])

            existing_ticker = Tickers.query.filter_by(symbol=symbol).first()

            if existing_ticker:
                existing_ticker.price = price

            else:
                new_ticker = Tickers(symbol=symbol, price=price)
                db.session.add(new_ticker)
        
        db.session.commit()

        return {"message": "table populated successfully"}
    
@ticker_table_ns.route('/tickers')
class Tickers(Resource):

    def get(self):
        api_key = "XNtTbIxyiAv3kKppkET8uuzRGLqa1DmNxh7mCDosiY41vkQu87nKzaTVfRgHS5C6"
        secret_key = "cfdm7bPCwJ5fzZZ15rqKcLjFFMz7Q9nk4rEpXwBeTo0LMFEQA2CLQoZh4zZI40Nv"
        # Create a Binance API client
        client = Client(api_key, secret_key)
    
        tickers = client.get_all_tickers()

        ticker_data = []

        for ticker in tickers: 
            symbol = ticker['symbol']
            price = float(ticker['price'])

            ticker_dict = {
                "symbol": symbol,
                "price": price
            }
            ticker_data.append(ticker_dict)
        
        return ticker_data
            
