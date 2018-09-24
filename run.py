import os
from api.app import create_app


app_config = os.getenv("ENV")
app = create_app(app_config)


if __name__ == "__main__":
    app.run()