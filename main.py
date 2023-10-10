from uagents import Agent, Context
from forex_python.converter import CurrencyRates
import time

currency_agent = Agent(name="currency_bot", seed="alice recovery phrase")

def get_exchange_rate(base_currency, foreign_currency):
    c = CurrencyRates()
    return c.get_rate(base_currency, foreign_currency)

@currency_agent.on_interval(period=60)  # Check every 60 seconds
async def on_interval(ctx: Context):
    if not ctx.storage.get("initialized"):
        # If not initialized, ask for user input
        base_currency = input("Enter your base currency: ")
        foreign_currencies = input("Enter foreign currencies to monitor (comma-separated): ").split(',')
        
        thresholds = {}
        for foreign_currency in foreign_currencies:
            upper = float(input(f"Set upper threshold for {base_currency} to {foreign_currency}: "))
            lower = float(input(f"Set lower threshold for {base_currency} to {foreign_currency}: "))
            thresholds[f"{base_currency}_{foreign_currency}"] = {'upper': upper, 'lower': lower}

        ctx.storage.set("base_currency", base_currency)
        ctx.storage.set("foreign_currencies", foreign_currencies)
        ctx.storage.set("thresholds", thresholds)
        ctx.storage.set("initialized", True)

    base_currency = ctx.storage.get("base_currency")
    foreign_currencies = ctx.storage.get("foreign_currencies")
    thresholds = ctx.storage.get("thresholds")

    for foreign_currency in foreign_currencies:
        rate = get_exchange_rate(base_currency, foreign_currency)
        threshold = thresholds.get(f"{base_currency}_{foreign_currency}")

        if rate > threshold['upper']:
            ctx.logger.info(f"Alert: {base_currency} to {foreign_currency} rate is above {threshold['upper']}")

        if rate < threshold['lower']:
            ctx.logger.info(f"Alert: {base_currency} to {foreign_currency} rate is below {threshold['lower']}")

if __name__ == "__main__":
    currency_agent.run()
