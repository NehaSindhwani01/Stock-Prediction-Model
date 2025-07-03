# 📈 Stock Price Prediction Tool

A Python-based application that allows users to **predict stock prices** using **Linear Regression**, powered by real-time data from **Yahoo Finance**. The tool features a fully interactive **GUI built with Pygame** and includes visual predictions using **Matplotlib**.

## 🚀 Features

- 🔎 Enter one or multiple stock symbols (e.g., `AAPL`, `TCS.NS`)
  
- 📊 Predict stock closing prices using historical data
  
- 🧠 Machine Learning model built with **Linear Regression**
  
- 📉 Displays actual vs. predicted prices on charts
  
- 🖥️ User-friendly GUI interface using **Pygame**
  
- 📂 Scrollable result view for multiple tickers
  
- ✅ Evaluation using **Mean Squared Error (MSE)**
  

## 🛠️ Technologies Used

- `Python`
  
- `yfinance` – Fetch real-time stock data

- `Matplotlib` – Plot prediction charts
  
- `Scikit-learn` – Linear Regression model
  
- `Pygame` – Build interactive GUI
  
- `NumPy`, `Pandas` – Data manipulation


## 📷 Screenshots
>[!Screeshot1](AAPL_char.png)
>[!Screeshot1](MSFT_char.png)
>[!Screeshot1](GOOG_char.png)

## 📦 Installation

1. Clone the repository:

git clone https://github.com//NehaSindhwani01/Stock-Prediction-Model.git

2. Install required libraries:

pip install pygame yfinance matplotlib scikit-learn numpy pandas

3. Run the application:

python main.py

## 🧠 How It Works

Downloads historical stock data (from Jan 2020 to Dec 2024)

Converts dates into numerical "Day Index"

Trains a linear regression model on historical data

Predicts future stock prices and plots them

Displays results with error metrics on GUI

## 🙋‍♀️ Author

Neha Sindhwani

