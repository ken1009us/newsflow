import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import json
import os
from typing import Tuple
from newsapi import NewsApiClient
from dash import html
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from dashNews.util import get_countries


news_api_key = os.environ.get("NEWS_API_KEY")
api = NewsApiClient(api_key=news_api_key)

countries = get_countries()
alpha_countries = sorted(countries)

items = alpha_countries[:-1]

try:
    default_top = api.get_top_headlines()
except Exception as e:
    print(f"Failed to fetch top headlines: {e}")
    default_top = {"articles": []}

top = default_top
news_dict = {}


def generate_chart(top: dict) -> px.scatter:
    """
    Generate a sentiment analysis scatter plot for the headlines.

    :param top: A dictionary containing top headlines.
    :return: A Plotly Express scatter plot object.
    """

    sia = SIA()
    headlines_results = []
    source_list_df = []

    for article in top["articles"]:
        title = article["title"]
        pol_score = sia.polarity_scores(title)
        pol_score["headline"] = title
        headlines_results.append(pol_score)
        source_list_df.append(article["source"]["name"])

    headline_df = pd.DataFrame.from_records(headlines_results)
    headline_df["source"] = source_list_df

    if not headline_df.empty:
        head_sent = px.scatter(
            headline_df,
            x="pos",
            y="neg",
            color="source",
            labels={"pos": "Positive", "neg": "Negative"},
            template="plotly_dark",
        )
        head_sent.update_traces(marker=dict(size=12), selector=dict(mode="markers"))
        head_sent.update_layout(title_text="Source Sentiment")
    else:
        head_sent = []

    return head_sent


def set_vars(location: str, query: str) -> Tuple[str, bool]:
    """
    Set the variables for location and query, returning the search result string and a boolean indicating if articles exist.

    :param location: The selected location.
    :param query: The search query.
    :return: A tuple containing the search result string and a boolean indicating if articles exist.
    """
    global top
    top = default_top

    search_res = "Top News Articles Worldwide"
    articles_exist = True

    if query is not None:
        top = api.get_top_headlines(q=query)
        search_res = f"Top News Articles with '{query}' Worldwide"

    if location is not None:
        top = api.get_top_headlines(country=countries[location]["newsid"])
        search_res = f"Top News Articles from {location}"

    if query is not None and location is not None:
        top = api.get_top_headlines(country=countries[location]["newsid"], q=query)
        search_res = f"Top News Articles with '{query}' from {location}"

    if not top["articles"]:
        top = default_top
        search_res = "No articles found."
        articles_exist = False

    return search_res, articles_exist


def generate_card(index: int) -> dbc.Card:
    """
    Generate a card component for an article.

    :param index: The index of the article in the global 'top' variable.
    :return: A Dash Bootstrap Components Card representing the article.
    """
    card = dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src=top["articles"][index]["urlToImage"],
                            className="img-fluid rounded-start",
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H4(
                                    top["articles"][index]["description"],
                                    className="card-text",
                                ),
                                dbc.Button(
                                    top["articles"][index]["source"]["name"],
                                    href=top["articles"][index]["url"],
                                    target="_blank",
                                    external_link=True,
                                    color="primary",
                                ),
                            ]
                        ),
                        className="col-md-8",
                    ),
                ],
                className="g-0 d-flex align-items-center",
            )
        ],
        className="mb-3",
        style={"maxWidth": "100%"},
    )

    return card


news_articles = []
for index, article in enumerate(top["articles"]):
    news_articles.append(
        dbc.AccordionItem(
            generate_card(0),
            title=top["articles"][index]["title"],
            item_id=f"item-{index}",
        )
    )

newsCards = dbc.Accordion(
    news_articles,
    id="accordion",
    active_item="item-1",
    flush=True,
    style={
        "width": "100%",
    },
)
