import dash_bootstrap_components as dbc
import dash
from dash import dcc, Input, Output, html, State

from dashNews.news_service import NewsService
from dashNews.countries import get_country_options
from dashNews.cards import generate_card
from dashNews.charts import generate_sentiment_chart
from dashNews.trends import get_trending_searches, build_trends_sidebar
from i18n import t, get_all

news_service = NewsService()
country_options = get_country_options()

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
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

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                "NewsFlow",
                style={
                    "font-family": "Kaushan Script",
                    "color": "white",
                    "fontSize": 45,
                    "font-weight": "bold",
                    "marginRight": 50,
                    "padding-right": 20,
                },
            ),
            dbc.Col(
                dbc.Input(
                    id="searchField",
                    placeholder=t("search_placeholder"),
                    size="md",
                    className="mb-3",
                    style={
                        "width": 150,
                        "height": 40,
                        "marginTop": 20,
                        "marginRight": 20,
                        "color": "black",
                    },
                ),
                width="auto",
            ),
            dbc.Col(
                dcc.Dropdown(
                    options=country_options,
                    id="country",
                    placeholder=t("country_placeholder"),
                    style={
                        "width": 150,
                        "height": 40,
                        "marginRight": 20,
                        "marginTop": 4,
                        "color": "black",
                    },
                ),
                width="auto",
            ),
            dbc.Col(
                dbc.Button(
                    t("search_button"),
                    id="searchButton",
                    className="me-2",
                    n_clicks=0,
                    style={"width": 80, "height": 40},
                ),
                width="auto",
            ),
            dbc.Col(
                dcc.Dropdown(
                    options=language_options,
                    id="language-selector",
                    value="en",
                    clearable=False,
                    style={
                        "width": 120,
                        "height": 40,
                        "marginTop": 4,
                        "color": "black",
                    },
                ),
                width="auto",
            ),
        ],
    ),
    color="dark",
    dark=True,
)

app.layout = html.Div(
    [
        dcc.Store(id="language-store", data="en"),
        navbar,
        dbc.Row(
            [html.H1(t("top_news_title"), id="title")],
            style={
                "marginLeft": 10,
                "marginBottom": 10,
                "marginTop": 25,
                "font-weight": 1000,
            },
        ),
        dbc.Row(
            [
                # Main news column (9/12)
                dbc.Col(
                    [
                        dcc.Loading(
                            id="loading-news",
                            type="circle",
                            children=[
                                dbc.Accordion(
                                    id="accordion",
                                    active_item="item-0",
                                    flush=True,
                                    style={"width": "100%"},
                                ),
                            ],
                        ),
                    ],
                    lg=9,
                    md=12,
                ),
                # Trends sidebar column (3/12)
                dbc.Col(
                    [
                        dcc.Loading(
                            id="loading-trends",
                            type="circle",
                            children=[
                                html.Div(id="trends-sidebar"),
                            ],
                        ),
                    ],
                    lg=3,
                    md=12,
                    style={"marginTop": "10px"},
                ),
            ],
            style={"marginLeft": 5, "marginRight": 5},
        ),
        dbc.Row(
            [
                dcc.Loading(
                    id="loading-chart",
                    type="circle",
                    children=[
                        dcc.Graph(id="set_graph"),
                    ],
                ),
            ],
            style={
                "marginRight": 20,
                "marginLeft": 20,
                "display": "flex",
                "flex-wrap": "wrap",
            },
        ),
        html.Footer(
            children=[
                html.P(
                    t("footer_copyright"),
                    id="footer-text",
                    style={"marginTop": "15px"},
                ),
                html.A(
                    html.Img(
                        src="/assets/linkedin.png",
                        style={"height": "30px", "width": "30px"},
                    ),
                    href="https://www.linkedin.com/in/shwu02",
                    style={"marginLeft": "10px"},
                    target="_blank",
                ),
                html.A(
                    html.Img(
                        src="/assets/github.png",
                        style={"height": "30px", "width": "30px"},
                    ),
                    href="https://github.com/ken1009us",
                    style={"marginLeft": "10px"},
                    target="_blank",
                ),
                html.A(
                    html.Img(
                        src="/assets/portfolio.png",
                        style={"height": "30px", "width": "30px"},
                    ),
                    href="https://www.ken-wu.com",
                    style={"marginLeft": "10px"},
                    target="_blank",
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "padding": "20px",
                "backgroundColor": "#333",
                "color": "white",
                "textAlign": "center",
                "left": 0,
                "bottom": 0,
                "width": "100%",
            },
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
        Output("accordion", "children"),
        Output("title", "children"),
        Output("set_graph", "figure"),
        Output("trends-sidebar", "children"),
    ],
    [
        Input("searchButton", "n_clicks"),
        Input("language-store", "data"),
    ],
    [State("searchField", "value"), State("country", "value")],
)
def update_page(n_clicks, lang, search_val, country_val):
    lang = lang or "en"
    lang_data = get_all(lang)

    try:
        title, articles = news_service.search_news(
            query=search_val,
            country=country_val,
        )

        if articles:
            # Build localized title
            from config import NEWSAPI_SUPPORTED_COUNTRIES

            country_name = NEWSAPI_SUPPORTED_COUNTRIES.get(country_val, "")
            if search_val and country_name:
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

            news_articles = [
                dbc.AccordionItem(
                    generate_card(article),
                    title=article.get("title") or lang_data.get(
                        "no_description", "No title"
                    ),
                    item_id=f"item-{index}",
                )
                for index, article in enumerate(articles)
            ]
            chart_figure = generate_sentiment_chart(articles)
        else:
            title = lang_data.get("no_articles_found", "No articles found.")
            news_articles = [
                html.Div(
                    lang_data.get("no_articles_message", "No articles found."),
                    style={"textAlign": "center", "marginTop": "2rem"},
                )
            ]
            chart_figure = generate_sentiment_chart([])

    except Exception as e:
        print(f"Error updating the page: {e}")
        news_articles = [
            html.Div(
                lang_data.get("error_message", "An error occurred."),
                style={
                    "textAlign": "center",
                    "marginTop": "2rem",
                    "color": "red",
                },
            )
        ]
        title = lang_data.get("error_title", "Error")
        chart_figure = generate_sentiment_chart([])

    # Build trends sidebar
    trends = get_trending_searches(country_val)
    trends_component = build_trends_sidebar(trends, lang_data)

    return news_articles, title, chart_figure, trends_component


@app.callback(
    [
        Output("searchField", "placeholder"),
        Output("searchButton", "children"),
        Output("footer-text", "children"),
    ],
    Input("language-store", "data"),
)
def update_ui_text(lang):
    lang = lang or "en"
    lang_data = get_all(lang)
    return (
        lang_data.get("search_placeholder", "News topics"),
        lang_data.get("search_button", "Go!"),
        lang_data.get("footer_copyright", ""),
    )


if __name__ == "__main__":
    app.run_server(debug=True)
