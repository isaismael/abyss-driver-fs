from flask import Flask
from app import create_app
from app.config import Config

app = create_app()

if __name__ == '__main__':
    app.config.from_object(Config)
    app.run()