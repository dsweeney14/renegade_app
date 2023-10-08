from flask_restx import Namespace, Resource
from flask import request, jsonify
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required
from models import AllPortfolio
from app import db

port_ns = Namespace('port', description="A namespace for the portfolios of the user")

# this is the model serialiser (exposes model in JSON format that the front end can read)
port_model = port_ns.model(
    "Portfolio", 
    {
        "id": fields.Integer(),
        "asset1": fields.String(),
        "asset2": fields.String(),
        "user_id": fields.Integer()
    }
)


@port_ns.route('/portfolios')
class PortResource(Resource):

    @port_ns.marshal_list_with(port_model)
    def get(self):
        """Get all portfolios from db """
        user_id = request.args.get("userId")

        portfolios = AllPortfolio.query.filter_by(user_id=user_id).all()
        return portfolios
    

    @port_ns.marshal_with(port_model)
    def post(self):
        """ Create a new portfolio """
        data = request.get_json()

        assets = data.get("entry")
        user_id = data.get("userId")

        asset1 = assets.get("Ticker1")
        asset2 = assets.get("Ticker2")
        
        existing_portfolio = AllPortfolio.query.filter_by(
            asset1=asset1, asset2=asset2, user_id=user_id
        ).first()

        if existing_portfolio:
            return existing_portfolio, 200  # Return existing portfolio if found
        else:
            new_portfolio = AllPortfolio(
                asset1=asset1,
                asset2=asset2,
                user_id=user_id
            )

            new_portfolio.save()

            db.session.commit()

            return new_portfolio, 201

@port_ns.route('/portfolios/<int:id>')
class PortResource(Resource):    

    @port_ns.marshal_with(port_model)
   
    def delete(self, id):
        """ Delete a portfolio """
        portfolio_to_delete = AllPortfolio.query.get_or_404(id)
        portfolio_to_delete.delete()

        return {"message": "Portfolio deteled."}

