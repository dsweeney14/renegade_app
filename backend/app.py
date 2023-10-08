from flask import Flask
from flask_restx import Api
from models import AllPortfolio, User, Tickers, TradeSignals
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from auth import auth_ns
from ticker_table import ticker_table_ns
from backtest_algorithm import backtest_ns
from port import port_ns
from recommendation_algorithm import signals_ns
from flask_cors import CORS
from config import DevConfig

def initiate_app(config):
        
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app)

    db.init_app(app)

    migrate = Migrate(app, db)

    JWTManager(app)

    api = Api(app, doc='/docs')

    api.add_namespace(auth_ns)
    api.add_namespace(ticker_table_ns)
    api.add_namespace(port_ns)
    api.add_namespace(backtest_ns)
    api.add_namespace(signals_ns)


    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db, 
            "Portfolio": AllPortfolio,
            "User": User,
            "Tickers": Tickers,
            "Trade Signals": TradeSignals
        }
    
    return app

app = initiate_app(DevConfig)

if __name__ == '__main__':
    app.run()