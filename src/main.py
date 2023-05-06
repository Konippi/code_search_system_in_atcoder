from config import log_config
from flask import Flask


app = Flask(
    __name__,
    static_folder="../frontend/static",
    template_folder="../frontend/templates",
)


if __name__ == "__main__":
    log_config.set_log_config()
    app.run(debug=True)
