from api import create_app
from os import getenv

environment = getenv("FLASK_ENV", "development")

app = create_app(environment)

if __name__ == "__main__":
    app.run()
