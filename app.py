import dash_bootstrap_components as dbc
import dash
from dash import dcc, Input, Output, html, State

from dashNews.news_service import NewsService
from dashNews.countries import get_country_options
from dashNews.timeline import build_timeline
from dashNews.wordcloud_gen import build_wordcloud_component
from dashNews.trends import get_trending_searches, build_trends_sidebar
from i18n import t, get_all

news_service = NewsService()
country_options = get_country_options()

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,
        "https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;600;700&display=swap",
    ],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0",
        }
    ],
)
server = app.server
app.title = "NewsFlow"

language_options = [
    {"label": "English", "value": "en"},
    {"label": "繁體中文", "value": "zh_tw"},
    {"label": "日本語", "value": "ja"},
]

# --- Navbar (sticky, instant search) ---
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A("NewsFlow", className="nf-navbar-brand", href="/"),
            html.Div(
                [
                    dbc.Input(
                        id="searchField",
                        placeholder=t("search_placeholder"),
                        size="md",
                        debounce=True,
                        className="nf-search-input",
                        style={"width": "200px", "marginRight": "10px"},
                    ),
                    html.Div(
                        dcc.Dropdown(
                            options=country_options,
                            id="country",
                            placeholder=t("country_placeholder"),
                            style={"width": "160px"},
                        ),
                        style={"marginRight": "10px"},
                    ),
                    html.Div(
                        dcc.Dropdown(
                            options=language_options,
                            id="language-selector",
                            value="en",
                            clearable=False,
                            style={"width": "120px"},
                        ),
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "flexWrap": "wrap",
                    "gap": "4px",
                },
            ),
        ],
        fluid=True,
        style={
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "space-between",
            "maxWidth": "1200px",
            "margin": "0 auto",
            "padding": "0 16px",
        },
    ),
    className="nf-navbar",
)

# --- Main Layout ---
app.layout = html.Div(
    [
        dcc.Store(id="language-store", data="en"),
        navbar,
        html.Div(
            [
                # Fallback notice
                html.Div(id="fallback-notice"),
                # Section title
                html.H3(
                    t("top_news_title"),
                    id="title",
                    className="nf-section-title",
                ),
                # Word cloud (full width)
                html.Div(id="wordcloud-container"),
                # Main content row
                dbc.Row(
                    [
                        # Timeline column (8/12)
                        dbc.Col(
                            [
                                dcc.Loading(
                                    id="loading-news",
                                    type="circle",
                                    color="#6b9fd4",
                                    children=[
                                        html.Div(id="news-timeline"),
                                    ],
                                ),
                            ],
                            lg=8,
                            md=12,
                        ),
                        # Trends sidebar (4/12)
                        dbc.Col(
                            [
                                dcc.Loading(
                                    id="loading-trends",
                                    type="circle",
                                    color="#6b9fd4",
                                    children=[
                                        html.Div(id="trends-sidebar"),
                                    ],
                                ),
                            ],
                            lg=4,
                            md=12,
                        ),
                    ],
                ),
            ],
            style={
                "maxWidth": "1200px",
                "margin": "0 auto",
                "padding": "0 16px 60px 16px",
            },
        ),
        # Fixed Footer
        html.Footer(
            children=[
                html.P(
                    t("footer_copyright"),
                    id="footer-text",
                ),
                html.A(
                    html.Img(src="/assets/linkedin.png"),
                    href="https://www.linkedin.com/in/shwu02",
                    target="_blank",
                ),
                html.A(
                    html.Img(src="/assets/github.png"),
                    href="https://github.com/ken1009us",
                    target="_blank",
                ),
                html.A(
                    html.Img(src="/assets/portfolio.png"),
                    href="https://www.ken-wu.com",
                    target="_blank",
                ),
            ],
            className="nf-footer",
        ),
    ]
)


@app.callback(
    Output("language-store", "data"),
    Input("language-selector", "value"),
)
def update_language_store(lang):
    return lang or "en"


@app.callback(
    [
        Output("news-timeline", "children"),
        Output("title", "children"),
        Output("trends-sidebar", "children"),
        Output("fallback-notice", "children"),
        Output("wordcloud-container", "children"),
    ],
    [
        Input("searchField", "value"),
        Input("country", "value"),
        Input("language-store", "data"),
    ],
)
def update_page(search_val, country_val, lang):
    lang = lang or "en"
    lang_data = get_all(lang)

    # Build trends sidebar
    trends_data = get_trending_searches(country_val)
    trends_component = build_trends_sidebar(trends_data, lang_data)

    fallback_notice = None
    wordcloud = None

    try:
        title, articles, fallback_type, original_country_name = (
            news_service.search_news(query=search_val, country=country_val)
        )

        if fallback_type and original_country_name:
            if fallback_type == "everything":
                notice_key = "country_fallback_everything"
                default_msg = (
                    "No top headlines for {country}. "
                    "Showing recent news about {country} instead."
                )
            else:
                notice_key = "country_fallback_notice"
                default_msg = (
                    "No results found for {country}. "
                    "Showing worldwide results instead."
                )
            notice_text = lang_data.get(
                notice_key, default_msg
            ).replace("{country}", original_country_name)
            fallback_notice = html.Div(
                notice_text, className="nf-fallback-notice"
            )

        if articles:
            from config import NEWSAPI_SUPPORTED_COUNTRIES

            country_name = NEWSAPI_SUPPORTED_COUNTRIES.get(country_val, "")
            if fallback_type == "worldwide":
                title = lang_data.get("top_news_worldwide", title)
                if search_val:
                    title = lang_data.get(
                        "top_news_with_query", title
                    ).replace("{query}", search_val)
            elif fallback_type == "everything":
                title = lang_data.get(
                    "news_about_country", "News about {country}"
                ).replace("{country}", country_name)
                if search_val:
                    title = lang_data.get(
                        "news_about_country_with_query",
                        "News about {country} with '{query}'"
                    ).replace("{country}", country_name).replace("{query}", search_val)
            elif search_val and country_name:
                title = lang_data.get(
                    "top_news_with_query_from_country", title
                ).replace("{query}", search_val).replace("{country}", country_name)
            elif search_val:
                title = lang_data.get(
                    "top_news_with_query", title
                ).replace("{query}", search_val)
            elif country_name:
                title = lang_data.get(
                    "top_news_from_country", title
                ).replace("{country}", country_name)
            else:
                title = lang_data.get("top_news_worldwide", title)

            timeline = build_timeline(articles, lang_data)
            wordcloud = build_wordcloud_component(articles)
        else:
            title = lang_data.get("no_articles_found", "No articles found.")
            timeline = html.Div(
                lang_data.get("no_articles_message", "No articles found."),
                style={
                    "textAlign": "center",
                    "marginTop": "2rem",
                    "color": "#8a8a88",
                },
            )

    except Exception as e:
        print(f"Error updating the page: {e}")
        timeline = html.Div(
            lang_data.get("error_message", "An error occurred."),
            style={
                "textAlign": "center",
                "marginTop": "2rem",
                "color": "#e25555",
            },
        )
        title = lang_data.get("error_title", "Error")

    return (
        timeline,
        title,
        trends_component,
        fallback_notice,
        wordcloud,
    )


@app.callback(
    [
        Output("searchField", "placeholder"),
        Output("footer-text", "children"),
    ],
    Input("language-store", "data"),
)
def update_ui_text(lang):
    lang = lang or "en"
    lang_data = get_all(lang)
    return (
        lang_data.get("search_placeholder", "News topics"),
        lang_data.get("footer_copyright", ""),
    )


if __name__ == "__main__":
    app.run_server(debug=True)
