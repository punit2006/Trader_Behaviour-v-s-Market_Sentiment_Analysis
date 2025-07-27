# 📊 Trader Behaviour vs Market Sentiment Analysis

This project explores the relationship between **trader behaviour** (based on historical trade data) and **market sentiment** (based on the Bitcoin Fear & Greed Index). It analyzes how market emotions impact trading outcomes like **Profit & Loss (PnL)** and **Trade Volume**.

---

## 📁 Project Structure

```bash
.
├── trader_behaviour_v_s_market_sentiment_analysis.py
├── csv_files/
│   └── merged_data.csv           # Merged trade and sentiment data
├── outputs/
│   ├── pnl_by_sentiment.png      # PnL vs Sentiment visualization
│   ├── volume_by_sentiment.png   # Volume vs Sentiment visualization
│   └── pnl_distribution_filtered.png # PnL distribution (outlier-filtered)
```

---

## 🔧 Requirements

* Python 3.x
* pandas
* numpy
* seaborn
* matplotlib

Install dependencies with:

```bash
pip install pandas numpy seaborn matplotlib
```

---

## 📌 How It Works

1. **Data Loading**
   Loads two datasets:

   * `historical_data.csv`: Trader transaction data
   * `fear_greed_index.csv`: Market sentiment data

2. **Preprocessing**

   * Formats dates
   * Standardizes columns
   * Calculates trade volume (tokens × price)

3. **Merging**
   Joins trade and sentiment datasets on the date field.

4. **Visualization**
   Generates:

   * PnL vs. Market Sentiment
   * Trade Volume vs. Market Sentiment
   * PnL Distribution (filtered between 1st and 99th percentile)

5. **Insights**

   * Compares average PnL and volume between **Greed** and **Fear** sentiment.
   * Highlights which sentiment yields better trading outcomes.

---

## 📊 Example Insights

* 📈 Higher **average PnL** during **Greed** suggests traders profit more in bullish sentiment.
* 🔄 Increased **volume** during **Greed** shows more market activity.
* Useful for quant strategies or sentiment-aware trading bots.

---

## ▶️ Usage

Run the script:

```bash
python trader_behaviour_v_s_market_sentiment_analysis.py
```

Ensure `historical_data.csv` and `fear_greed_index.csv` are placed in the appropriate directory or update the path in the script.

---

## 🧠 Key Takeaways

* Sentiment classification ("Fear" or "Greed") significantly influences trader performance.
* Integrating sentiment with trading data provides actionable insights for risk management and strategy optimization.

---
## CSV_FILES

fear_greed_index : https://drive.google.com/file/d/1tqHB1jpkbKIfOS5Wcazvl_pwwfAXvLvW/view?usp=sharing

historical_data : https://drive.google.com/file/d/1hnMoYilDVY7MSteBtV9yObzlKKXMb5_3/view?usp=sharing

---

## 📮 Contact

For questions or collaboration:

✉️ Linkedin: www.linkedin.com/in/punitjain163
📬 Email: punit163.work@gmail.com
