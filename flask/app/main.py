from flask import Flask, render_template
from api import bp as api_blueprint
from flask_cors import CORS

app = Flask(__name__, static_folder="./../static/", template_folder="./../template/")
cors = CORS(app)
app.register_blueprint(api_blueprint)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return 'PLAN.EXE'


if __name__ == "__main__":
    app.run(port=5000, debug=True)
