import dash_bootstrap_components as dbc
from dash import html

PLACEHOLDER_IMAGE = "https://placehold.co/400x250/242426/8a8a88?text=No+Image"


def generate_card(article: dict, lang_data: dict = None) -> dbc.Card:
    """Generate a card component for a single article.

    Args:
        article: A dict with keys like 'title', 'description', 'urlToImage',
                 'url', 'source', and 'publishedAt'.
        lang_data: Translation dict for UI strings.

    Returns:
        A dbc.Card component.
    """
    if lang_data is None:
        lang_data = {}

    image_url = article.get("urlToImage") or PLACEHOLDER_IMAGE
    description = article.get("description") or lang_data.get(
        "no_description", "No description available."
    )
    source_name = (article.get("source") or {}).get("name", "Unknown")
    article_url = article.get("url") or "#"
    published_at = article.get("publishedAt") or ""

    # Format date: "2025-01-15T10:30:00Z" → "2025-01-15"
    date_display = published_at[:10] if published_at else ""

    card_body_children = []

    if date_display:
        card_body_children.append(
            html.P(date_display, className="nf-card-date mb-1")
        )

    card_body_children.append(
        html.P(description, className="nf-card-description")
    )

    card_body_children.append(
        dbc.Button(
            source_name,
            href=article_url,
            target="_blank",
            external_link=True,
            className="nf-card-source-btn",
        )
    )

    card = dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src=image_url,
                            className="img-fluid rounded-start",
                            style={
                                "objectFit": "cover",
                                "height": "100%",
                                "minHeight": "160px",
                            },
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        dbc.CardBody(card_body_children),
                        className="col-md-8",
                    ),
                ],
                className="g-0 d-flex align-items-stretch",
            )
        ],
        className="nf-card mb-3",
    )

    return card
