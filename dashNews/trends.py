import dash_bootstrap_components as dbc
from dash import html

# Mapping from NewsAPI country codes to Google Trends geo/pn codes
# Google Trends uses different identifiers for trending searches
COUNTRY_TO_TRENDS_PN = {
    "ar": "argentina",
    "au": "australia",
    "at": "austria",
    "be": "belgium",
    "br": "brazil",
    "ca": "canada",
    "co": "colombia",
    "cz": "czech_republic",
    "eg": "egypt",
    "fr": "france",
    "de": "germany",
    "gr": "greece",
    "hk": "hong_kong",
    "hu": "hungary",
    "in": "india",
    "id": "indonesia",
    "ie": "ireland",
    "il": "israel",
    "it": "italy",
    "jp": "japan",
    "kr": "south_korea",
    "my": "malaysia",
    "mx": "mexico",
    "nl": "netherlands",
    "nz": "new_zealand",
    "ng": "nigeria",
    "no": "norway",
    "ph": "philippines",
    "pl": "poland",
    "pt": "portugal",
    "ro": "romania",
    "rs": "serbia",
    "ru": "russia",
    "sa": "saudi_arabia",
    "sg": "singapore",
    "za": "south_africa",
    "se": "sweden",
    "ch": "switzerland",
    "tw": "taiwan",
    "th": "thailand",
    "tr": "turkey",
    "ua": "ukraine",
    "gb": "united_kingdom",
    "us": "united_states",
    "ve": "venezuela",
}


def get_trending_searches(country_code: str = None) -> list:
    """Fetch Google trending searches for a given country.

    Args:
        country_code: NewsAPI-style country code (e.g. 'us', 'jp').
                      Defaults to 'us' if None or not mapped.

    Returns:
        A list of trending search strings, or empty list on error.
    """
    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="en-US", tz=360)

        pn = COUNTRY_TO_TRENDS_PN.get(country_code, "united_states")
        df = pytrends.trending_searches(pn=pn)

        return df[0].tolist()[:20]
    except Exception as e:
        print(f"Google Trends error: {e}")
        return []


def build_trends_sidebar(trends: list, lang_data: dict = None) -> dbc.Card:
    """Build a sidebar card component displaying trending searches.

    Args:
        trends: List of trending search strings.
        lang_data: Translation dict for UI strings.

    Returns:
        A dbc.Card component for the sidebar.
    """
    title = "Trending Searches"
    if lang_data:
        title = lang_data.get("trending_searches", title)

    if not trends:
        no_data = "No trending data available."
        if lang_data:
            no_data = lang_data.get("no_trending_data", no_data)
        body_content = [html.P(no_data, className="text-muted")]
    else:
        body_content = [
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(
                        [
                            html.Span(
                                f"{i + 1}. ",
                                style={"fontWeight": "bold", "marginRight": "8px"},
                            ),
                            html.Span(trend),
                        ],
                        style={
                            "backgroundColor": "transparent",
                            "border": "none",
                            "borderBottom": "1px solid #444",
                            "color": "white",
                            "padding": "8px 12px",
                        },
                    )
                    for i, trend in enumerate(trends)
                ],
                flush=True,
            )
        ]

    return dbc.Card(
        [
            dbc.CardHeader(
                html.H5(title, className="mb-0", style={"color": "white"}),
                style={"backgroundColor": "#375a7f"},
            ),
            dbc.CardBody(
                body_content,
                style={
                    "backgroundColor": "#303030",
                    "maxHeight": "600px",
                    "overflowY": "auto",
                    "padding": "0",
                },
            ),
        ],
        style={"border": "1px solid #444"},
    )
