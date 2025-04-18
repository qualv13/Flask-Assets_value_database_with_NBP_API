# 🏦 Flask Assets Value Database with NBP API

This is a simple Flask web application that allows users to store and manage their asset data in different currencies and convert asset values based on **yesterday's average exchange rates** using data from the [NBP API (Narodowy Bank Polski)](http://api.nbp.pl).

## 🧪 How It Works

1. You add an asset (e.g. 100 USD, 200 EUR).
2. The app fetches **yesterday’s exchange rate** from NBP API.
3. The value is converted to PLN and saved along with the original.
4. You can view, update, or delete assets anytime.

## 📌 Features

- Add, edit, and delete asset records
- Store asset value in various currencies
- Automatically convert asset values to PLN using NBP API (based on **yesterday's** mid-rate)
- Lightweight and easy to set up

## 🧰 Technologies Used

- **Python 3**
- **Flask** – Web framework
- **Flask-SQLAlchemy** – ORM for database interaction
- **Flask-WTF** – Form rendering and validation
- **SQLite** – Local database
- **NBP API** – For currency conversion based on mid exchange rates

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/qualv13/Flask-Assets_value_database_with_NBP_API.git
cd Flask-Assets_value_database_with_NBP_API
```

### 2. (Optional but recommended) Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # On Linux/Mac
venv\Scripts\activate           # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```


## 🛠️ Running the Application

### 1. Initialize the database

Start the app once to automatically create the `assets.db` file:

```bash
python app.py
```

You should see output like:
```bash
* Running on http://127.0.0.1:5000/
```

### 2. Open in browser
Go to http://127.0.0.1:5000/ to use the application.

### 3. Have fun and try it yourself!

## 💡 Notes

- Currency rates are retrieved using **NBP’s Table A (mid rates)**.
- Exchange rate used is always for **yesterday** (excluding weekends/holidays).
- Values are **not auto-updated** after they're stored.
- Make sure the currency code is supported by the NBP API.


## ✅ Supported Currencies

NBP supports most major currencies like:

- USD, EUR, GBP, CHF, JPY, AUD, CAD, SEK, NOK, CZK, DKK, HUF, etc.

You can check the full list here:  
[http://api.nbp.pl/api/exchangerates/tables/A/?format=json](http://api.nbp.pl/api/exchangerates/tables/A/?format=json)

## 📬 Author

Developed by [qualv13](https://github.com/qualv13)  
This project is licensed under the **MIT License**.
