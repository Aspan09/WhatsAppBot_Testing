import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    SELENIUM_URL = "https://green-api.com/docs/"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.getenv('USER')}:{os.getenv('PASSWORD')}@"
        f"{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GREEN_API_URL = os.getenv('GREEN_API_URL')
