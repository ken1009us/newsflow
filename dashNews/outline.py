from newsapi import NewsApiClient
from dash import dcc, Input, Output, html, State
from IPython import display
from pprint import pprint
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from dashNews.tweets import get_trending_tweets, get_countries

import dash_bootstrap_components as dbc
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


countries = get_countries()
alpha_countries = []
for country in countries:
    alpha_countries.append(country)

alpha_countries.sort()

items = []
for location in alpha_countries:
    items.append(location)
items.pop()

api = NewsApiClient(api_key='202a98452ccb402784fa6cd0a7d3772a')

default_top = api.get_top_headlines()
top = api.get_top_headlines()

default_tweets = get_trending_tweets(1)
tweets = get_trending_tweets(1)

tweets_dict = {}
news_dict = {}

def generateChart(top):
    headlines = set()
    sourceListDf = []
    for title in top['articles']:
        headlines.add(title['title'])
        sourceListDf.append(title['source']['name'])

    sia = SIA()
    headlinesResults = []

    for line in headlines:
        pol_score_h = sia.polarity_scores(line)
        pol_score_h['headline'] = line
        headlinesResults.append(pol_score_h)

    headlineDf = pd.DataFrame.from_records(headlinesResults)
    headlineDf["source"] = sourceListDf
    if not headlineDf.empty:
        headSent = px.scatter(headlineDf, x="pos", y="neg", color="source", labels={"pos":"Positive","neg":"Negative"})
        headSent.update_traces(marker=dict(size=12),
                               selector=dict(mode='markers'))
        headSent.update_layout(title_text="Source Sentiment")
    else:
        headSent = []

    return headSent

def setVars(location, query):
    global tweets
    global top
    top = default_top
    tweets = default_tweets

    search_res = "Top News Articles Worldwide"
    tweets_res = "Trending Tweets Worldwide"

    if location is None:
        tweets = default_tweets
    else:
        if location in tweets_dict:
            tweets = tweets_dict[location]
        else:
            tweets = get_trending_tweets(countries[location]["twitterid"])
            tweets_dict[location] = tweets

        tweets_res = "Trending Tweets from {}".format(location)

    if query is not None and location is not None:
        if query != '':
            top = api.get_top_headlines(country=countries[location]["newsid"], q=query)
            if not top['articles']:
                if location in news_dict:
                    top = news_dict[location]
                else:
                    top = api.get_top_headlines(country=countries[location]["newsid"])
                    news_dict[location] = top
                search_res = "Top News Articles from {}".format(location)
            else:
                search_res = "Top News Articles with '{}' from {}".format(query, location)
        else:
            query = None

    if query is None and location is not None:
        if location in news_dict:
            top = news_dict[location]
        else:
            top = api.get_top_headlines(country=countries[location]["newsid"])
            news_dict[location] = top
        search_res = "Top News Articles from {}".format(location)

    if query is not None and location is None:
        top = api.get_top_headlines(q=query)
        search_res = "Top News Articles with '{}' Worldwide".format(query)

    if not top['articles']:
        top = default_top
        search_res = "Top News Articles Worldwide"

    return search_res, tweets_res


def generateCard(i):
    card = dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src=top['articles'][i]['urlToImage'],
                            className="img-fluid rounded-start",
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H4(top['articles'][i]['description'], className="card-text"),
                                dbc.Button(
                                    top['articles'][i]['source']['name'],
                                    href=top['articles'][i]['url'],
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
for index, article in enumerate(top['articles']):
    news_articles.append(dbc.AccordionItem(
        generateCard(0),
        title=top['articles'][index]['title'],
        item_id="item-{}".format(index),
    ))

newsCards = dbc.Accordion(
    news_articles,
    id="accordion",
    active_item="item-1",
    flush=True,
    style={'width': "76%", }
)

hold_tweet_list = []
hold_tweet_list.append(dbc.ListGroupItem([
    html.Div(
        [
            html.H5("Trending Tweets", className="mb-1"),
        ],
        className="d-flex w-100 justify-content-between",
    ),
]), )

for i in range(10):
    hold_tweet_list.append(dbc.ListGroupItem(tweets[i]['name'], href=tweets[i]['url']))

tweetList = dbc.ListGroup(
    hold_tweet_list,
    style={"width": "20%","marginLeft":40},
    id="tweetList",
)
