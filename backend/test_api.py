import unittest
from app import initiate_app
from config import TestConfig
from exts import db
import json
import pandas as pd

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = initiate_app(TestConfig)

        self.client = self.app.test_client(self)

        with self.app.app_context():
            db.create_all()

    def test_register(self):
        register_response = self.client.post('/auth/register',             
            json = {"username": "testusername", 
                    "email" : "testusername@email.com", 
                    "password" : "password"}
        )
        status_code = register_response.status_code
        self.assertEqual(status_code, 201)

    def test_login(self):
        register_response = self.client.post('/auth/register',             
            json = {"username": "testusername", 
                    "email" : "testusername@email.com", 
                    "password" : "password"}
        ) 

        login_response = self.client.post('/auth/login', 
            json = {"username": "testusername", 
                    "password": "password"}
        )
        status_code = login_response.status_code
        self.assertEqual(status_code, 200)

    def test_get_all_portfolios(self):
        response = self.client.get('/port/portfolios')
        status_code = response.status_code
        self.assertEqual(status_code, 200)


    def test_create_portfolio(self):
        register_response = self.client.post('/auth/register',             
            json = {"username": "testusername", 
                    "email" : "testusername@email.com", 
                    "password" : "password"}
        ) 

        login_response = self.client.post('/auth/login', 
            json = {"username": "testusername", 
                    "password": "password"}
        )
        access_token = login_response.json["access_token"]

        create_portfolio_response = self.client.post('/port/portfolios',
            json = {
                "entry": {
                    "Ticker1": "BTC/USDT",
                    "Ticker2": "ETH/USDT",
                },
                "userId": 1
            }, 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        
        status_code = create_portfolio_response._status
        self.assertEqual(status_code, '201 CREATED')

    def test_delete_portfolio(self):
        register_response = self.client.post('/auth/register',             
            json = {"username": "testusername", 
                    "email" : "testusername@email.com", 
                    "password" : "password"}
        ) 

        login_response = self.client.post('/auth/login', 
            json = {"username": "testusername", 
                    "password": "password"}
        )
        access_token = login_response.json["access_token"]

        create_portfolio_response = self.client.post('/port/portfolios',
            json = {
                "entry": {
                    "Ticker1": "BTC/USDT",
                    "Ticker2": "ETH/USDT",
                },
                "userId": 1
            }, 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )

        id = 1
        
        delete_response = self.client.delete(f'/port/portfolios/{id}',
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        status_code = delete_response.status_code
        self.assertEqual(status_code, 200)
    
    def test_backtest_algorithm(self):
        expected_data = [
            'MDT/USDT, COMP/USDT, 10.10, 66.70',
            'BUSD/USDT, COMP/USDT, 7.53, 43.86',
            'BNB/USDT, COMP/USDT, 6.97, 33.10',
            'BNB/USDT, MDT/USDT, 6.34, 34.17',
            'BNB/USDT, FIL/USDT, 6.17, 27.81',
            'BUSD/USDT, MDT/USDT, 6.10, 22.97',
            'FIL/USDT, MDT/USDT, 5.71, 44.66',
            'FIL/USDT, COMP/USDT, 5.61, 42.56',
            'XVG/USDT, MDT/USDT, 4.26, 41.85',
            'BCH/USDT, BNB/USDT, 4.00, 27.60',
            'LTC/USDT, BNB/USDT, 3.63, 13.21',
            'XVG/USDT, BUSD/USDT, 3.35, 37.12',
            'BUSD/USDT, FIL/USDT, 3.18, 11.90',
            'BNB/USDT, BUSD/USDT, 3.17, 5.60',
            'BCH/USDT, BUSD/USDT, 2.99, 15.92',
            'LTC/USDT, FIL/USDT, 2.62, 17.29',
            'BCH/USDT, COMP/USDT, 2.62, 19.64',
            'XVG/USDT, FIL/USDT, 2.15, 20.03',
            'BTC/USDT, BNB/USDT, 1.13, 2.81',
            'LTC/USDT, BUSD/USDT, 0.80, 2.75',
            'BTC/USDT, BUSD/USDT, 0.34, 0.37',
            'ETH/USDT, BUSD/USDT, 0.01, -0.07',
            'ETH/USDT, BNB/USDT, -0.18, -0.71'
        ]

        # Convert the strings to DataFrame
        expected_df = pd.DataFrame([item.split(', ') for item in expected_data], columns=["Ticker 1", "Ticker 2", "Sharpe Ratio", "Cumulative Returns"])
        expected_df['Sharpe Ratio'] = expected_df['Sharpe Ratio'].astype(float)
        expected_df['Cumulative Returns'] = expected_df['Cumulative Returns'].astype(float)
        with self.app.app_context():
            backtest_response = self.client.get('/backtest/initiate')
            backtest_data = backtest_response.get_json()
            backtest_data = backtest_data.replace("\/", "/")
            backtest_data = backtest_data.replace("Ticker1", "Ticker 1")
            backtest_data = backtest_data.replace("Ticker2", "Ticker 2")

            data_objects = backtest_data.strip().split('\n')
            parsed_data = []
            for object in data_objects:
                parsed_data.append(json.loads(object))

            backtest_df = pd.DataFrame(parsed_data)
            backtest_df['Sharpe Ratio'] = backtest_df['Sharpe Ratio'].astype(float)
            backtest_df['Cumulative Returns'] = backtest_df['Cumulative Returns'].astype(float)

            self.assertTrue((backtest_df == expected_df).all().all(), "DataFrames are not equal")

    def test_cancel_analysis(self):
        response = self.client.post('/backtest/initiate')
        self.assertEqual(response.json, 'Program cancelled by user', "Response JSON message should match")
        self.assertEqual(response.status_code, 200)

    def test_post_trade_signal(self):
        expected_json = {
            "portfolio_id": None,  
            "time": None,  
            "asset_price1": None,  
            "asset_price2": None,  
            "zscore": None,  
            "recommendation": None  
        }

        response = self.client.post('/trade/initiate',
            json = {"id": 1, 
                    "asset1": "MDT/USDT",
                    "asset2": "COMP/USDT"}   
        )
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json, expected_json)
        
    def test_query_trade_signal(self):
        populate_trade_table = self.client.post('/trade/initiate',
            json = {"id": 1, 
                    "asset1": "MDT/USDT",
                    "asset2": "COMP/USDT"}   
        )

        id = 1
        response = self.client.get(f'/trade/trades/{id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_trade_signal(self):
        populate_trade_table = self.client.post('/trade/initiate',
            json = {"id": 1, 
                    "asset1": "MDT/USDT",
                    "asset2": "COMP/USDT"}   
        )

        id = 1
        response = self.client.delete(f'/trade/trades/{id}')
        self.assertEqual(response.status_code, 200)

        
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()