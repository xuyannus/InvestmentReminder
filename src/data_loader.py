import quandl

API_KEY = 'AFqzqWCyRmeY1Ex-PH6s'


def get_us_stock_historical_price(symbol, start_date, end_date):
    quandl.ApiConfig.api_key = API_KEY
    return quandl.get(symbol.upper(), start_date=start_date, end_date=end_date)
