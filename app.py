from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__, template_folder='HTML/templates')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
