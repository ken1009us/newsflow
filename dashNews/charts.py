import pandas as pd
import plotly.graph_objects as go
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


# Custom light template for the Japanese minimalist theme
NF_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(
            family="Noto Sans JP, Helvetica Neue, Arial, sans-serif",
            color="#2c2c2c",
            size=12,
        ),
        xaxis=dict(
            gridcolor="#eeeeec",
            linecolor="#d5d5d3",
            zerolinecolor="#d5d5d3",
        ),
        yaxis=dict(
            gridcolor="#eeeeec",
            linecolor="#d5d5d3",
            zerolinecolor="#d5d5d3",
        ),
    )
)


def generate_sentiment_chart(articles: list, lang_data: dict = None) -> go.Figure:
    """Generate a compact horizontal bar chart of headline sentiment scores."""
    if lang_data is None:
        lang_data = {}

    if not articles:
        return _empty_figure(lang_data)

    sia = SIA()
    records = []

    for article in articles:
        title = article.get("title") or ""
        if not title.strip():
            continue

        source_name = (article.get("source") or {}).get("name", "Unknown")
        pol_score = sia.polarity_scores(title)
        records.append({
            "headline": title[:45] + ("..." if len(title) > 45 else ""),
            "full_headline": title,
            "source": source_name,
            "compound": pol_score["compound"],
        })

    if not records:
        return _empty_figure(lang_data)

    df = pd.DataFrame.from_records(records)
    df = df.sort_values("compound", ascending=True)

    # Color: positive → indigo, negative → red, neutral → gray
    colors = [
        "#2b4c7e" if c > 0.05 else "#c53030" if c < -0.05 else "#a0a09e"
        for c in df["compound"]
    ]

    positive_label = lang_data.get("positive", "Positive")
    negative_label = lang_data.get("negative", "Negative")
    neutral_label = lang_data.get("neutral", "Neutral")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["compound"],
            y=df["headline"],
            orientation="h",
            marker=dict(
                color=colors,
                line=dict(width=0),
            ),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "%{customdata[1]}<br>"
                "%{x:.2f}"
                "<extra></extra>"
            ),
            customdata=list(zip(df["full_headline"], df["source"])),
        )
    )

    # Compact height: 25px per bar, min 200, max 400
    chart_height = min(400, max(200, len(records) * 25 + 60))

    fig.update_layout(
        template=NF_TEMPLATE,
        xaxis=dict(
            title="",
            range=[-1, 1],
            dtick=0.5,
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            title="",
            automargin=True,
            tickfont=dict(size=10),
        ),
        height=chart_height,
        margin=dict(l=10, r=10, t=10, b=30),
        bargap=0.35,
        showlegend=False,
    )

    # Zero line (dashed)
    fig.add_vline(
        x=0,
        line_dash="dash",
        line_color="#d5d5d3",
        line_width=1,
    )

    # Legend annotations: colored squares with labels
    fig.add_annotation(
        x=1, y=1.02, xref="paper", yref="paper",
        text=(
            f"<span style='color:#c53030'>\u25a0</span> {negative_label}  "
            f"<span style='color:#a0a09e'>\u25a0</span> {neutral_label}  "
            f"<span style='color:#2b4c7e'>\u25a0</span> {positive_label}"
        ),
        showarrow=False,
        font=dict(size=11),
        xanchor="right",
        yanchor="bottom",
    )

    return fig


def _empty_figure(lang_data: dict = None) -> go.Figure:
    """Return an empty light-themed figure with a message."""
    if lang_data is None:
        lang_data = {}

    fig = go.Figure()
    fig.update_layout(
        template=NF_TEMPLATE,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=150,
        margin=dict(l=10, r=10, t=10, b=10),
        annotations=[
            dict(
                text=lang_data.get("no_data_available", "No data available"),
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=14, color="#a0a09e"),
            )
        ],
    )
    return fig
