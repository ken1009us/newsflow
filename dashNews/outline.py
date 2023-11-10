from newsapi import NewsApiClient
from dash import dcc, Input, Output, html, State
from IPython import display
from pprint import pprint
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from dashNews.util import get_countries

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

countries = get_countries()
alpha_countries = []
for country in countries:
    alpha_countries.append(country)

alpha_countries.sort()

items = []
for location in alpha_countries:
    items.append(location)
items.pop()

api = NewsApiClient(api_key="XXXXXX")

default_top = api.get_top_headlines()
top = api.get_top_headlines()
news_dict = {}


def generate_chart(top):
    headlines = set()
    source_list_df = []
    for title in top["articles"]:
        headlines.add(title["title"])
        source_list_df.append(title["source"]["name"])

    sia = SIA()
    headlines_results = []

    for line in headlines:
        pol_score_h = sia.polarity_scores(line)
        pol_score_h["headline"] = line
        headlines_results.append(pol_score_h)

    headline_df = pd.DataFrame.from_records(headlines_results)
    headline_df["source"] = source_list_df
    if not headline_df.empty:
        head_sent = px.scatter(
            headline_df,
            x="pos",
            y="neg",
            color="source",
            labels={"pos": "Positive", "neg": "Negative"},
        )
        head_sent.update_traces(marker=dict(size=12), selector=dict(mode="markers"))
        head_sent.update_layout(title_text="Source Sentiment")
    else:
        head_sent = []

    return head_sent


def set_vars(location, query):
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


def generate_card(i):
    card = dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src=top["articles"][i]["urlToImage"],
                            className="img-fluid rounded-start",
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H4(
                                    top["articles"][i]["description"],
                                    className="card-text",
                                ),
                                dbc.Button(
                                    top["articles"][i]["source"]["name"],
                                    href=top["articles"][i]["url"],
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
