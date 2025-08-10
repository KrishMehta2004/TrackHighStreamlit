# TrackHigh: 52-Week High NSE Stock Dashboard

![TrackHigh Logo](https://img.icons8.com/ios-filled/100/ffffff/line-chart.png)

**TrackHigh** is a modern, interactive Streamlit dashboard for tracking and analyzing stocks on the National Stock Exchange (NSE) that have hit their 52-week highs. With a beautiful UI, advanced filtering, and insightful visualizations, TrackHigh empowers investors and analysts to discover high-performing stocks, analyze sector/industry trends, and monitor returns with ease.

---

## 🚀 Features

- **Track 52-Week Highs:** Instantly view which NSE stocks have hit their 52-week highs.
- **Flexible Views:** Analyze by specific date, month, date range, or search for individual stocks.
- **Advanced Filtering:** Filter by sector, series, and sort by returns, market cap, P/E, and more.
- **Modern Visuals:** Beautiful, futuristic UI with interactive charts (Plotly) and custom CSS.
- **Stock Cards:** Detailed cards for each stock, including sector, industry, price, returns, and more.
- **Sector & Industry Analysis:** Visualize sector and industry distributions for high performers.
- **Performance Tables:** See most frequent high performers and their returns.
- **Responsive Design:** Works great on desktop and mobile.

---

## 📸 Screenshots

> _Add screenshots or GIFs of your dashboard here for maximum impact!_

---

## 🛠️ Tech Stack

- **Frontend/UI:** [Streamlit](https://streamlit.io/)
- **Data Processing:** [Polars](https://www.pola.rs/), [NumPy](https://numpy.org/)
- **Visualization:** [Plotly](https://plotly.com/python/)
- **Data Source:** [TrackHigh_Data CSV](https://github.com/KrishMehta2004/TrackHigh_Data)

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/TrackHighStreamlit.git
   cd TrackHighStreamlit
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run main.py
   ```

---

## ⚙️ Usage

- On launch, the dashboard loads the latest NSE 52-week high data.
- Use the sidebar to select your view:
  - **Specific Date:** See all stocks at 52-week highs on a chosen date.
  - **Month:** Analyze trends and top performers for a month.
  - **Date Range:** Track highs over any custom period.
  - **Search Stock:** Dive deep into a specific stock’s high points and performance.
- Filter and sort results as needed.
- Explore interactive charts and detailed stock cards.

---

## 🧩 Project Structure

```
TrackHighStreamlit/
│
├── main.py            # Streamlit app entry point
├── components.py      # UI components (cards, charts, metrics)
├── views.py           # View logic for each dashboard mode
├── data_loader.py     # Data loading and preprocessing
├── data_processing.py # Data analysis utilities
├── utilities.py       # Formatting helpers
├── requirements.txt   # Python dependencies
└── README.md          # This file!
```

---

## 🌐 Data Source

- Data is loaded from:  
  [TrackHigh_Data CSV](https://github.com/KrishMehta2004/TrackHigh_Data/refs/heads/main/Data.csv)
- The app automatically fetches and processes the latest data on launch.

---

## 📝 Customization

- **Add new metrics:** Edit `components.py` and `views.py` to display more stock KPIs.
- **Change data source:** Update the URL in `data_loader.py`.
- **Styling:** Tweak the custom CSS in `main.py` for a different look.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to fork the repo and submit a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Polars](https://www.pola.rs/)
- [Plotly](https://plotly.com/python/)
- [NSE India](https://www.nseindia.com/)
