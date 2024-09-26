from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
from io import StringIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    api_key = 'v4f341dfffejr7c6srvo8xozf9gz4mtp1kcwxzwo'
    url = f"https://api.ja.is/search/v6/?q={query}&scope=businesses&count=10000&start=1"
    headers = {
        'Authorization': api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        business_items = data.get('items', [])
        return jsonify(business_items)
    return jsonify({'error': 'Failed to fetch data from API'}), 500

@app.route('/export', methods=['POST'])
def export():
    results = request.json.get('results', [])
    df = pd.DataFrame(results)
    csv_data = StringIO()
    df.to_csv(csv_data, index=False)
    csv_data.seek(0)
    return csv_data.getvalue(), 200, {'Content-Disposition': 'attachment; filename=results.csv'}

if __name__ == "__main__":
    app.run(debug=True)
