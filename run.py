from api.app import create_app


config_name = "staging"
app = create_app("staging")


if __name__ == "__main__":
    app.run()