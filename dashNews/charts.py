import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


def generate_sentiment_chart(articles: list) -> go.Figure:
    """Generate a sentiment analysis scatter plot for article headlines.

    Args:
        articles: List of article dicts, each with 'title' and 'source' keys.

    Returns:
        A Plotly Figure. Returns an empty figure if no valid articles.
    """
    if not articles:
        return _empty_figure()

    sia = SIA()
    records = []

    for article in articles:
        title = article.get("title") or ""
        if not title.strip():
            continue

        source_name = (article.get("source") or {}).get("name", "Unknown")
        pol_score = sia.polarity_scores(title)
        pol_score["headline"] = title
        pol_score["source"] = source_name
        records.append(pol_score)

    if not records:
        return _empty_figure()

    df = pd.DataFrame.from_records(records)

    fig = px.scatter(
        df,
        x="pos",
        y="neg",
        color="source",
        hover_data=["headline"],
        labels={"pos": "Positive", "neg": "Negative"},
        template="plotly_dark",
    )
    fig.update_traces(marker=dict(size=12), selector=dict(mode="markers"))
    fig.update_layout(title_text="Source Sentiment")

    return fig


def _empty_figure() -> go.Figure:
    """Return an empty dark-themed figure with a message."""
    fig = go.Figure()
    fig.update_layout(
        template="plotly_dark",
        title_text="Source Sentiment",
        xaxis_title="Positive",
        yaxis_title="Negative",
        annotations=[
            dict(
                text="No data available",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16, color="gray"),
            )
        ],
    )
    return fig
