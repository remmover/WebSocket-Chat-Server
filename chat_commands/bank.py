import argparse
from datetime import datetime, timedelta
import pprint
import platform
import asyncio

import aiohttp




# parser = argparse.ArgumentParser(description="Currency exchange rates in recent days")
# parser.add_argument('--course', '-c', help="Enter num", required=True)
# parser.add_argument('currency', nargs='*', help="Currency code")
# args = parser.parse_args()


def desired_date(num_days):
    end_date = datetime.now().date()
    dates = []
    for _ in range(num_days):
        dates.append(end_date.strftime("%d.%m.%Y"))
        end_date -= timedelta(days=1)
    return dates


def parse_message(message):
    parts = message.split(" ")
    num_days = int(parts[1])
    currency = parts[2:]
    return num_days, currency


async def fetch_exchange_rates(session, date, results, currencies):
    try:
        async with session.get(
            f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"
        ) as response:
            if response.status == 200:
                result = await response.json()
                await process_exchange_rates(result, results, currencies)
            else:
                print(f"Error status: {response.status} for privatbank")
    except aiohttp.ClientConnectorError as err:
        print(f"Connection error: privatbank", str(err))


async def process_exchange_rates(result, results, currencies):
    currency_rates = {}
    target_currencies = ["EUR", "USD"] + currencies

    for rate in result["exchangeRate"]:
        currency = rate["currency"]
        if currency in target_currencies:
            purchase_rate = rate.get("purchaseRate", rate["purchaseRateNB"])
            sale_rate = rate.get("saleRate", rate["saleRateNB"])
            currency_rates[currency] = {"purchase": purchase_rate, "sale": sale_rate}
    results.append({result["date"]: currency_rates})


async def main(message):
    num_days, currencies = parse_message(message)
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        if num_days >= 10:
            print("Error: The value of 'course' argument must be less than 10.")
            exit(1)
        dates = desired_date(num_days)
        for date in dates:
            tasks.append(fetch_exchange_rates(session, date, results, currencies))
        await asyncio.gather(*tasks)
    return results


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main("exchange 2 KZT"))
    pprint.pprint(r)
