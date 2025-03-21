import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
from flask import Flask, render_template, jsonify, send_from_directory
import io
import base64
import os

app = Flask(__name__, static_folder='C:\\tEHMEH\\static')

def prepare_data(file_name):
    file_path = os.path.join(r'C:\tEHMEH\data', file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist. Please check the file name and path.")
    
    data = pd.read_csv(file_path)
    
    date_formats = ['%d-%m-%Y', '%Y-%m-%d', '%m-%d-%Y']
    for date_format in date_formats:
        try:
            data['Date'] = pd.to_datetime(data['Date'], format=date_format)
            break
        except ValueError:
            continue
    
    if not pd.api.types.is_datetime64_any_dtype(data['Date']):
        raise ValueError(f"Unable to parse the Date column in {file_name}. Please check the date format in the CSV file.")
    
    data = data.sort_values(by='Date')
    data['Price'] = data['Price'].str.replace(',', '').astype(float)
    data['Next_Day_Close'] = data['Price'].shift(-1)
    data = data.dropna()
    return data

def train_model(data):
    X = data[['Price']].values
    y = data['Next_Day_Close'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model, X_test, y_test

def generate_plot(data, y_test, y_pred, company):
    plt.figure(figsize=(14, 7))
    plt.style.use('dark_background')
    plt.plot(data['Date'][-len(y_test):], y_test, label='Actual Close Price', color='white')
    plt.plot(data['Date'][-len(y_test):], y_pred, label='Predicted Close Price', color='#3498db', linestyle='--')
    plt.title(f"{company}: Actual vs Predicted Close Price (Test Data)", fontsize=16, color='white')
    plt.xlabel("Date", fontsize=12, color='white')
    plt.ylabel("Close Price (₹)", fontsize=12, color='white')
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7, color='gray')
    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, facecolor='black', edgecolor='none')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

def generate_regression_plot(data, model, company):
    plt.figure(figsize=(14, 7))
    plt.style.use('dark_background')
    plt.scatter(data['Price'], data['Next_Day_Close'], alpha=0.5, color='white')
    plt.plot(data['Price'], model.predict(data[['Price']]), color='#3498db', linewidth=2)
    plt.title(f"{company}: Linear Regression Model on Close Price", fontsize=16, color='white')
    plt.xlabel("Today's Close Price (₹)", fontsize=12, color='white')
    plt.ylabel("Next Day's Close Price (₹)", fontsize=12, color='white')
    plt.grid(True, linestyle='--', alpha=0.7, color='gray')
    plt.tight_layout()
    
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, facecolor='black', edgecolor='none')
    img.seek(0)
    regression_plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return regression_plot_url

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/')
def index():
    companies = {
        'TCS': 'TCS Historical Data.csv',
        'ADEL': 'ADEL Historical Data.csv',
        'BRLC': 'BRLC Historical Data.csv'
    }
    
    results = {}
    errors = {}
    
    for company, file_name in companies.items():
        try:
            data = prepare_data(file_name)
            model, X_test, y_test = train_model(data)
            y_pred = model.predict(X_test)
            
            last_close_price = data['Price'].iloc[-1]
            next_day_price = model.predict([[last_close_price]])[0]
            mse = mean_squared_error(y_test, y_pred)
            
            plot_url = generate_plot(data, y_test, y_pred, company)
            regression_plot_url = generate_regression_plot(data, model, company)
            
            results[company] = {
                'next_day_price': f"{next_day_price:.2f}",
                'mse': f"{mse:.4f}",
                'plot_url': plot_url,
                'regression_plot_url': regression_plot_url,
                'last_date': data['Date'].iloc[-1].strftime('%d %B %Y'),
                'last_price': f"{last_close_price:.2f}"
            }
        except Exception as e:
            errors[company] = str(e)
    
    return render_template('index.html', results=results, errors=errors)

if __name__ == '__main__':
    app.run(debug=True)