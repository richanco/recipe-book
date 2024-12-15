import os
from flask import Flask, request
import awsgi
from recipe_search import recipe_search
from flask import render_template

app = Flask(__name__)

app.json.ensure_ascii = False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    request_ingredients = request.args.get('ingredients').split()
    print(request_ingredients)
    return render_template('saved.html',recipe_list =recipe_search(*request_ingredients))

# この前に関数を定義すること
def lambda_handler(event,context):
    return awsgi.response(app,event,context)

# ローカル環境で実行する場合
if os.getenv('ENV') == 'local':
    app.run(debug=True)