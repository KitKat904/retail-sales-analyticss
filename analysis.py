import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def load_data():
    return pd.read_csv("data/sales.csv")

def clean_data(data):
    data.dropna(inplace=True)
    return data

def analyze_data(data):
    total = data['Sales'].sum()
    monthly = data.groupby('Month')['Sales'].sum()
    return total, monthly

def product_sales(data):
    return data.groupby('Product')['Sales'].sum()

def store_sales(data):
    return data.groupby('Store')['Sales'].sum()

#  ADVANCED ML FORECAST
def ml_forecast(monthly):
    X = np.arange(len(monthly)).reshape(-1, 1)
    y = monthly.values

    model = LinearRegression()
    model.fit(X, y)

    # Predict next 3 months
    future_X = np.arange(len(monthly), len(monthly) + 3).reshape(-1, 1)
    predictions = model.predict(future_X)

    return predictions