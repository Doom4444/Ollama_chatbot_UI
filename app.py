from flask import Flask, send_from_directory
from api.chat_routes import chat_bp

app = Flask(__name__, static_folder="static")

app.register_blueprint(chat_bp)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)