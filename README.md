# Newsflow

Newsflow is a web application that aggregates trending news articles and provides a search interface for users to find news related to specific topics or from specific countries.

![image](https://github.com/ken1009us/newsflow/blob/main/assets/homepage.png "homepage")

#### Link:  <http://www.newsflow-app.com/>

### Inspiration:
With the overwhelming amount of information available online, staying updated with the latest news can be challenging. Newsflow was built to simplify this process by providing a user-friendly platform to access trending news and search for articles on topics of interest across different countries.

### What it does:
The application displays trending news articles and features a search bar where users can type keywords related to their desired news or select countries to filter articles geographically.

### How I built it:
Newsflow is built with Python using the Dash framework, which is ideal for building data-driven web applications. The application integrates the NewsAPI to fetch real-time news articles. The front-end utilizes Dash Bootstrap Components to create a responsive and visually appealing user interface.

### Features
- Displays trending news articles from various sources.
- Search functionality to find news by keywords or phrases.
- Country filter to view news from selected geographical locations.
- Sentiment analysis to gauge the tone of news articles.


## For Developers

Developers interested in contributing to the Newsflow project or setting up their own version can follow the steps below to get started.

### Prerequisites
- Python 3.9 or higher
- Virtual environment (recommended)
- API key from [NewsAPI](https://newsapi.org/)

### Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install some modules.

```bash
pip install -r requirements.txt
```

### Preparation

Before running the application, you need to import the necessary libraries and modules, including newsapi, dash, outline, dash_bootstrap_components, requests, and base64, pycountry.

### Execution
Run the application with:
```
(venv) $ python app.py
```

After starting the server, open your web browser and navigate to http://localhost:XXXX (replace XXXX with the port number provided in the terminal) to view the application.

Now you are ready to go!

## Possible improvements
Probably would be cool to incorporate some analytics, improve UI/UX, and get more API requests.
