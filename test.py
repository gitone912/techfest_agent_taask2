from forex_python.converter import CurrencyRates
import time

def get_exchange_rate(base_currency, foreign_currency):
    c = CurrencyRates()
    return c.get_rate(base_currency, foreign_currency)

def monitor_exchange_rates(base_currency, foreign_currencies, thresholds):
    while True:
        for foreign_currency in foreign_currencies:
            rate = get_exchange_rate(base_currency, foreign_currency)
            threshold = thresholds.get(f"{base_currency}_{foreign_currency}")

            if rate > threshold['upper']:
                print(f"Alert: {base_currency} to {foreign_currency} rate is above {threshold['upper']}")

            if rate < threshold['lower']:
                print(f"Alert: {base_currency} to {foreign_currency} rate is below {threshold['lower']}")

        time.sleep(60)  # Sleep for 60 seconds before checking again

if __name__ == "__main__":
    base_currency = input("Enter your base currency: ")
    foreign_currencies = input("Enter foreign currencies to monitor (comma-separated): ").split(',')
    
    thresholds = {}
    for foreign_currency in foreign_currencies:
        upper = float(input(f"Set upper threshold for {base_currency} to {foreign_currency}: "))
        lower = float(input(f"Set lower threshold for {base_currency} to {foreign_currency}: "))
        thresholds[f"{base_currency}_{foreign_currency}"] = {'upper': upper, 'lower': lower}

    monitor_exchange_rates(base_currency, foreign_currencies, thresholds)
