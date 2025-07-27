# Trader Behavior vs. Market Sentiment Analysis

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings

warnings.filterwarnings('ignore')

def load_and_preprocess_data():
    # Load datasets
    trades_df = pd.read_csv("/content/historical_data.csv")
    sentiment_df = pd.read_csv("/content/fear_greed_index.csv")

    # Preprocess Sentiment Data
    sentiment_df.columns = sentiment_df.columns.str.strip()
    if 'timestamp' in sentiment_df.columns:
        sentiment_df['timestamp'] = pd.to_datetime(sentiment_df['timestamp'], unit='s')
        sentiment_df['date'] = sentiment_df['timestamp'].dt.date
    elif 'date' in sentiment_df.columns:
        sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.date
    else:
        raise ValueError("Neither 'timestamp' nor 'date' column found in sentiment_df.")

    if 'classification' in sentiment_df.columns:
        sentiment_df['classification'] = sentiment_df['classification'].str.strip().str.capitalize()
    else:
        raise ValueError("'classification' column not found in sentiment_df.")

    # Preprocess Trader Data
    trades_df.columns = trades_df.columns.str.strip()
    if 'Timestamp IST' in trades_df.columns:
        trades_df['Timestamp IST'] = pd.to_datetime(trades_df['Timestamp IST'], format="%d-%m-%Y %H:%M")
        trades_df['date'] = trades_df['Timestamp IST'].dt.date
    elif 'Timestamp' in trades_df.columns:
        trades_df['Timestamp'] = pd.to_datetime(trades_df['Timestamp'], unit='s')
        trades_df['date'] = trades_df['Timestamp'].dt.date
    else:
        raise ValueError("Neither 'Timestamp IST' nor 'Timestamp' column found in trades_df.")

    if 'Side' in trades_df.columns:
        trades_df['side'] = trades_df['Side'].str.lower()
    else:
        trades_df['side'] = 'unknown'

    if 'Closed PnL' in trades_df.columns:
        trades_df['PnL'] = trades_df['Closed PnL']
    else:
        trades_df['PnL'] = np.nan

    if 'Size Tokens' in trades_df.columns and 'Execution Price' in trades_df.columns:
        trades_df['Volume'] = trades_df['Size Tokens'] * trades_df['Execution Price']
    elif 'size' in trades_df.columns and 'execution price' in trades_df.columns:
        trades_df['Volume'] = trades_df['size'] * trades_df['execution price']
    else:
        trades_df['Volume'] = np.nan

    return trades_df, sentiment_df

def merge_data(trades_df, sentiment_df):
    if 'date' in trades_df.columns and 'date' in sentiment_df.columns:
        merged_data = pd.merge(trades_df, sentiment_df[['date', 'classification']], on='date', how='left')
        return merged_data
    else:
        raise ValueError("'date' column not found in trades_df or sentiment_df.")

def save_merged_data(df):
    os.makedirs("csv_files", exist_ok=True)
    df.to_csv("csv_files/merged_data.csv", index=False)
    print("Merged data saved to csv_files/merged_data.csv")
    print("")

def generate_visualizations(df):
    os.makedirs("outputs", exist_ok=True)

    if not df[['classification', 'PnL']].isnull().all().any() and not df.empty:
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=df, x='classification', y='PnL')
        plt.title("Closed PnL by Market Sentiment")
        plt.savefig("outputs/pnl_by_sentiment.png")
        plt.show()
        print("")
    else:
        print("Warning: Could not generate PnL boxplot.")

    if not df[['classification', 'Volume']].isnull().all().any() and not df.empty:
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=df, x='classification', y='Volume')
        plt.title("Trade Volume by Market Sentiment")
        plt.savefig("outputs/volume_by_sentiment.png")
        plt.show()
    else:
        print("Warning: Could not generate Volume boxplot.")

def generate_insights(df):
    if 'classification' in df.columns and 'PnL' in df.columns and 'Volume' in df.columns and not df.empty:
        if {'Greed', 'Fear'}.issubset(df['classification'].unique()):
            pnl_greed = df[df['classification'] == 'Greed']['PnL'].mean()
            pnl_fear = df[df['classification'] == 'Fear']['PnL'].mean()
            volume_greed = df[df['classification'] == 'Greed']['Volume'].mean()
            volume_fear = df[df['classification'] == 'Fear']['Volume'].mean()

            print("\n📌 Key Insights:")
            print(f"→ Average PnL during Greed: {pnl_greed:.2f}")
            print(f"→ Average PnL during Fear: {pnl_fear:.2f}")
            print(f"→ Average Trade Volume during Greed: {volume_greed:.2f}")
            print(f"→ Average Trade Volume during Fear: {volume_fear:.2f}")

            if pnl_greed > pnl_fear:
                print("✅ Traders are more profitable during GREED periods.")
            if volume_greed > volume_fear:
                print("📈 Market activity (volume) is higher during GREED.")
        else:
            print("⚠️ Not enough classification variety for comparison.")
    else:
        print("⚠️ Not enough data for insights.")

def main():
    try:
        trades_df, sentiment_df = load_and_preprocess_data()
        df = merge_data(trades_df, sentiment_df)
        save_merged_data(df)
        generate_visualizations(df)
        generate_insights(df)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

# Optional: filter extreme outliers using IQR or percentiles
p1 = np.percentile(df['PnL'], 1)
p99 = np.percentile(df['PnL'], 99)

# Clip values between 1st and 99th percentile
filtered_df = df[(df['PnL'] >= p1) & (df['PnL'] <= p99)]

# Plot
plt.figure(figsize=(10, 6))
sns.histplot(data=filtered_df, x='PnL', bins=50, kde=True, color='skyblue')
plt.title("PnL Distribution (1st to 99th Percentile)")
plt.xlabel("Profit and Loss per Trade")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/pnl_distribution_filtered.png")
plt.show()

