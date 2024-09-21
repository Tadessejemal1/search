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
    url = f"https://api.ja.is/search/v6/?q={query}"
    headers = {
        'Authorization': api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        business_items = data.get('businesses', {}).get('items', [])
        return jsonify(business_items)
    return jsonify({'error': 'Failed to fetch data from API'}), 500

@app.route('/export', methods=['POST'])
def export_to_csv():
    results = request.json.get('results')
    if not results:
        return jsonify({'error': 'No data to export'}), 400
    
    df = pd.DataFrame(results)
    output = StringIO()
    df.to_csv(output, index=False)
    return output.getvalue(), 200

if __name__ == '__main__':
    app.run(debug=True)
