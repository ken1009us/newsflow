import dash_bootstrap_components as dbc
import dash
from dash import dcc, Input, Output, html, State
from dashNews import outline


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server
app.title = "NewsFlow"

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
                    "marginRight": 150,
                    "padding-right": 60,
                },
            ),
            dbc.Col(
                dbc.Input(
                    id="searchField",
                    placeholder="News topics",
                    size="md",
                    className="mb-3",
                    style={
                        "width": 500,
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
                    outline.items,
                    id="country",
                    placeholder="Country",
                    style={
                        "height": 40,
                        "marginRight": 20,
                        "marginTop": 4,
                        "color": "black",
                    },
                ),
                width=3,
            ),
            dbc.Col(
                dbc.Button(
                    "Go!",
                    id="searchButton",
                    className="me-2",
                    n_clicks=0,
                    style={"width": 60, "height": 40},
                )
            ),
        ]
    ),
    color="dark",
    dark=True,
)

app.layout = html.Div(
    [
        navbar,
        dbc.Row(
            [html.H1("Top News Articles", id="title")],
            style={
                "marginLeft": 10,
                "marginBottom": 10,
                "marginTop": 25,
                "font-weight": 1000,
            },
        ),
        dbc.Row(
            [outline.newsCards],
            id="main_row",
        ),
        dbc.Row(
            [
                dcc.Graph(id="set_graph", figure=outline.generate_chart(outline.top)),
            ],
            style={"marginRight": 20},
        ),
        html.Footer(
            children=[
                html.P(
                    "© NewsFlow 2023, Author: Shu-Hao (Ken) Wu",
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
                    href="https://portfolio-ken1009us.vercel.app/",
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
                # "position": "fixed",
                "left": 0,
                "bottom": 0,
                "width": "100%",
            },
        ),
    ]
)


@app.callback(
    [
        Output("accordion", "children"),
        Output("title", "children"),
        Output("set_graph", "figure"),
    ],
    [Input("searchButton", "n_clicks")],
    [State("searchField", "value"), State("country", "value")],
)
def update_page(n_clicks: int, searchVal: str, countryVal: str) -> tuple:
    """
    Updates the page content based on the search value and country value.

    :param n_clicks: The number of times the search button has been clicked.
    :param searchVal: The value of the search input field.
    :param countryVal: The value of the country dropdown.
    :return: A tuple containing the new accordion children, title text, and graph figure.
    """
    # if n_clicks is None or (searchVal is None or searchVal.strip() == ""):
    #     raise dash.exceptions.PreventUpdate

    try:
        new_title, articles_exist = outline.set_vars(countryVal, searchVal)
        if articles_exist:
            top = outline.top
            news_articles = [
                dbc.AccordionItem(
                    outline.generate_card(index),
                    title=article["title"],
                    item_id=f"item-{index}",
                )
                for index, article in enumerate(top["articles"])
            ]

            chart_figure = outline.generate_chart(top)
        else:
            news_articles = [
                html.Div(
                    "No articles found. Please try a different search or check your filters.",
                    style={"textAlign": "center", "marginTop": "2rem"},
                )
            ]
            chart_figure = {}
    except Exception as e:
        # If there's an error during the update, log it and provide a user-friendly message
        print(f"Error updating the page: {e}")
        news_articles = [
            html.Div(
                "An error occurred while fetching articles. Please try again later.",
                style={"textAlign": "center", "marginTop": "2rem", "color": "red"},
            )
        ]
        new_title = "Error"
        chart_figure = {}

    return news_articles, new_title, chart_figure


if __name__ == "__main__":
    # host="0.0.0.0", port="8050"
    # app.run_server(debug=False, host="0.0.0.0", port="8050")
    app.run_server()
