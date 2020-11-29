from flask import Flask, render_template
app = Flask(__name__, static_folder="./../static/", template_folder="./../template/")

@app.route('/')
def index():
    return render_template("index.html", title="Главная")


@app.route('/preparation')
def preparation():
    return render_template("index.html", title="Подготовка")


@app.route('/conduct')
def conduct():
    return render_template("index.html", title="Проведение")


@app.route('/processing')
def processing():
    return render_template("index.html", title="Обработка")


@app.route('/data')
def data():
    return render_template("index.html", title="Данные")


@app.route('/completion')
def completion():
    return render_template("index.html", title="Завершение")



if __name__ == "__main__":
    app.run(port=5000, debug=True)
