import dash_bootstrap_components as dbc
from dash import html

PLACEHOLDER_IMAGE = "https://via.placeholder.com/300x200?text=No+Image"


def generate_card(article: dict) -> dbc.Card:
    """Generate a card component for a single article.

    Args:
        article: A dict with keys like 'title', 'description', 'urlToImage',
                 'url', and 'source'.

    Returns:
        A dbc.Card component.
    """
    image_url = article.get("urlToImage") or PLACEHOLDER_IMAGE
    description = article.get("description") or "No description available."
    source_name = (article.get("source") or {}).get("name", "Unknown")
    article_url = article.get("url") or "#"

    card = dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src=image_url,
                            className="img-fluid rounded-start",
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H4(
                                    description,
                                    className="card-text",
                                ),
                                dbc.Button(
                                    source_name,
                                    href=article_url,
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
