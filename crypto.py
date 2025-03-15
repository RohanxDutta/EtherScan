import requests
import pandas as pd
from datetime import datetime, timedelta
#Some important libraries

def fetch_crypto(coin_id, days=730):
    #Fetch data from coingecko.
    '''This i get free, as you guided from Etherscan that was paid version, so i used this.'''

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    parameter = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    response = requests.get(url, params=parameter)

    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")
    
    data = response.json()
    df = pd.DataFrame(data['prices'], columns=["timestamp", "price"])
    df['volume'] = [v[1] for v in data['total_volumes']]
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.drop(columns=['timestamp'])
    return df

import seaborn as sns
import matplotlib.pyplot as plt

def plot_crypto_data(df, coin_name):
    """Visualize price trends and volume for a cryptocurrency"""
    sns.set_theme(style="darkgrid")

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()
    
    sns.lineplot(x=df['date'], y=df['price'], ax=ax1, color='blue', label='Price (INR)')
    sns.barplot(x=df['date'], y=df['volume'], ax=ax2, color='gray', alpha=0.3, label='Volume')
    
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price (INR)", color='blue')
    ax2.set_ylabel("Volume", color='gray')
    ax1.set_title(f"{coin_name} Price and Volume Trend (Last {len(df)} Days)")
    ax1.tick_params(axis='y', labelcolor='blue')
    ax2.tick_params(axis='y', labelcolor='black')
    
    plt.legend()
    plt.show()



def main():
    """User input for cryptocurrency selection and visualization."""

    coin_dict = {"ETH": "ethereum", "DOGE": "dogecoin", "XRP": "ripple", "SOL": "solana"}
    print("Available coins: ETH, DOGE, XRP, SOL")
    user_input = input("Enter the coin symbol: ").strip().upper()
    
    if user_input not in coin_dict:
        print("Invalid coin symbol!")
        return
    
    days = int(input("Enter the number of past days to fetch data for (1-730): "))
    df = fetch_crypto(coin_dict[user_input], days)
    plot_crypto_data(df, user_input)

if __name__ == "__main__":
    main()