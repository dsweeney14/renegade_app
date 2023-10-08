from exts import db
from sqlalchemy import ForeignKey


"""
Build the model for users 
"""
class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    username = db.Column(db.String(25), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.Text(), nullable = False)

    def __repr__(self):
        return f"<User {self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit() 

"""
Build the database model for the ticker table
""" 
class Tickers(db.Model):
    symbol = db.Column(db.String(10), nullable=False, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Tickers {self.symbol}: {self.price}>"

"""
Build the database model for portfolios
""" 
class AllPortfolio(db.Model):
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='portfolios')
    asset1=db.Column(db.String(), nullable=False)
    asset2=db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Portfolio {self.asset1} - {self.asset2}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

"""
Build the database model for the trade signals table
""" 
class TradeSignals(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    portfolio_id = db.Column(db.Integer(), ForeignKey(AllPortfolio.id), nullable=False)
    portfolio = db.relationship('AllPortfolio', backref='trade_signal_tables')
    time = db.Column(db.String())
    asset_price1 = db.Column(db.Float(), nullable=True)
    asset_price2 = db.Column(db.Float(), nullable=True)
    zscore = db.Column(db.Float(), nullable=True)
    recommendation = db.Column(db.String, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()