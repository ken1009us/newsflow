import time
import dash_bootstrap_components as dbc
from dash import html

# In-memory cache: {geo: {"trends": [...], "timestamp": float}}
_trends_cache = {}
_CACHE_TTL = 300  # 5 minutes


def get_trending_searches(country_code: str = None) -> dict:
    """Fetch Google trending searches for a given country using trendspy.

    Returns:
        A dict with keys:
        - "trends": list of trending search strings
        - "error": None, "rate_limited", or "general_error"
    """
    geo = (country_code or "us").upper()

    # Check cache
    cached = _trends_cache.get(geo)
    if cached and (time.time() - cached["timestamp"]) < _CACHE_TTL:
        return {"trends": cached["trends"], "error": None}

    # Try up to 2 times
    for attempt in range(2):
        try:
            from trendspy import Trends

            tr = Trends()
            trending = tr.trending_now(geo=geo)
            trends = [item.keyword for item in trending][:20]

            # Update cache
            _trends_cache[geo] = {
                "trends": trends,
                "timestamp": time.time(),
            }

            return {"trends": trends, "error": None}

        except Exception as e:
            error_str = str(e).lower()
            is_rate_limit = (
                "429" in error_str
                or "rate" in error_str
                or "too many" in error_str
            )

            if is_rate_limit and attempt < 1:
                time.sleep(2)
                continue

            print(f"Google Trends error (attempt {attempt + 1}): {e}")

            error_type = "rate_limited" if is_rate_limit else "general_error"
            return {"trends": [], "error": error_type}

    return {"trends": [], "error": "general_error"}


def build_trends_sidebar(trends_data: dict, lang_data: dict = None) -> dbc.Card:
    """Build a sidebar card component displaying trending searches.

    Args:
        trends_data: Dict with "trends" and "error" keys.
        lang_data: Translation dict for UI strings.
    """
    if lang_data is None:
        lang_data = {}

    title = lang_data.get("trending_searches", "Trending Searches")
    trends = trends_data.get("trends", [])
    error = trends_data.get("error")

    body_content = []

    # Show error notice if applicable
    if error == "rate_limited":
        msg = lang_data.get(
            "trends_rate_limited",
            "Trending data is temporarily unavailable.",
        )
        body_content.append(
            html.Div(msg, className="nf-trends-error")
        )
    elif error == "general_error" and not trends:
        no_data = lang_data.get("no_trending_data", "No trending data available.")
        body_content.append(
            html.P(no_data, className="text-muted", style={"padding": "14px 18px"})
        )

    if trends:
        import urllib.parse

        body_content.append(
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(
                        html.A(
                            [
                                html.Span(f"{i + 1}", className="nf-trends-rank"),
                                html.Span(trend),
                            ],
                            href=f"https://www.google.com/search?q={urllib.parse.quote_plus(trend)}",
                            target="_blank",
                        ),
                        className="nf-trends-item",
                    )
                    for i, trend in enumerate(trends)
                ],
                flush=True,
            )
        )

    return dbc.Card(
        [
            dbc.CardHeader(
                html.H5(title, className="mb-0"),
                className="nf-trends-header",
            ),
            dbc.CardBody(
                body_content,
                className="nf-trends-body",
            ),
        ],
        className="nf-trends-card",
    )
