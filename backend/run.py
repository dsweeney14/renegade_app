from app import initiate_app
from config import DevConfig, ProdConfig

if __name__ == "__main__":
    app = initiate_app(DevConfig)
    app.run()