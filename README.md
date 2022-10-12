# Newsflow

Newsflow is a web application that aggregates trending news articles and provides a search interface for users to find news related to specific topics or from specific countries.

![image](https://github.com/ken1009us/newsflow/blob/main/assets/homepage.png "homepage")

### Features

- Displays trending news articles from various sources
- Search functionality to find news by keywords or phrases
- Country filter to view news from selected geographical locations (54 NewsAPI-supported countries)
- Sentiment analysis scatter plot to gauge the tone of news headlines
- Google Trends sidebar showing trending searches by country
- Multi-language support (English, 繁體中文, 日本語)

## For Developers

### Prerequisites

- Python 3.9 or higher
- Virtual environment (recommended)
- API key from [NewsAPI](https://newsapi.org/)

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Copy the example environment file and add your API key:

```bash
cp .env.example .env
```

Edit `.env` and set your `NEWS_API_KEY`.

### Running Locally

```bash
export NEWS_API_KEY=your_api_key_here
python app.py
```

Open your browser and navigate to the URL shown in the terminal (default: http://127.0.0.1:8050).

### Deployment (Render)

1. Push the repository to GitHub.
2. Create a new Web Service on [Render](https://render.com/).
3. Connect your GitHub repository.
4. Set the `NEWS_API_KEY` environment variable in Render's dashboard.
5. Render will use `render.yaml` for build and start commands automatically.

### Project Structure

```
newsflow/
├── app.py                    # Main Dash app (layout + callbacks)
├── config.py                 # Centralized settings (env vars, constants)
├── dashNews/
│   ├── __init__.py
│   ├── news_service.py       # NewsAPI wrapper (lazy init, no global state)
│   ├── charts.py             # Sentiment analysis chart
│   ├── cards.py              # News card component
│   ├── countries.py          # NewsAPI-supported countries list
│   └── trends.py             # Google Trends sidebar
├── i18n/
│   ├── __init__.py           # Translation loader + t() helper
│   ├── en.json               # English
│   ├── zh_tw.json            # 繁體中文
│   └── ja.json               # 日本語
├── assets/                   # Static images
├── requirements.txt
├── render.yaml               # Render deployment config
├── Procfile
├── runtime.txt
└── nltk.txt
```
