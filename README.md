# NewsFlow

A modern news aggregation app built with Dash, featuring a dark Japanese minimalist (和風極簡) design. Aggregates trending news via NewsAPI with multi-country support, Google Trends integration, word clouds, and multi-language UI.

![image](https://github.com/ken1009us/newsflow/blob/main/assets/homepage.png "homepage")

### Features

- **Instant Search** — debounce-based search triggers on Enter or blur (no button needed)
- **54-Country Support** — with 3-tier fallback: top headlines → country-related news → worldwide
- **Timeline View** — vertical timeline with relative timestamps, sorted newest first
- **Accordion Card View** — expandable article cards with images, descriptions, and source links
- **Word Cloud** — generated from article titles with a blue theme matching the dark UI
- **Google Trends Sidebar** — real-time trending searches via `trendspy`, clickable to Google
- **Multi-Language** — English, 繁體中文, 日本語 (i18n with JSON)
- **Dark Mode** — full dark theme with Noto Sans JP / Noto Serif JP typography

## For Developers

### Prerequisites

- Python 3.9 or higher
- API key from [NewsAPI](https://newsapi.org/)

### Installation

```bash
python3 -m venv venv
source venv/bin/activate
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
source venv/bin/activate
python3 app.py
```

Open http://127.0.0.1:8050 in your browser.

### Deployment (Render)

1. Push the repository to GitHub.
2. Create a new **Web Service** on [Render](https://render.com/).
3. Connect your GitHub repository.
4. Set the **Build Command**: `pip install -r requirements.txt`
5. Set the **Start Command**: `gunicorn app:server`
6. Add the `NEWS_API_KEY` environment variable in Render's dashboard.
7. Deploy — Render will auto-detect `render.yaml` if present.

### Project Structure

```
newsflow/
├── app.py                    # Main Dash app (layout + callbacks)
├── config.py                 # Centralized settings (env vars, 54 countries)
├── dashNews/
│   ├── __init__.py
│   ├── news_service.py       # NewsAPI wrapper with 3-tier fallback
│   ├── cards.py              # Accordion card component
│   ├── timeline.py           # Vertical timeline component
│   ├── wordcloud_gen.py      # Word cloud image generator
│   ├── countries.py          # Country dropdown options
│   └── trends.py             # Google Trends via trendspy (cached)
├── i18n/
│   ├── __init__.py           # Translation loader + t() / get_all()
│   ├── en.json               # English
│   ├── zh_tw.json            # 繁體中文
│   └── ja.json               # 日本語
├── assets/
│   └── custom.css            # Dark mode theme (和風極簡)
├── requirements.txt
├── render.yaml               # Render deployment config
├── Procfile
├── runtime.txt
└── .env.example
```
