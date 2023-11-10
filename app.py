import dash_bootstrap_components as dbc
import dash

from dash import dcc, Input, Output, html, State
from dashNews import outline

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
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
                    },
                ),
                width="auto",
            ),
            dbc.Col(
                dcc.Dropdown(
                    outline.items,
                    id="country",
                    placeholder="Country",
                    style={"height": 40, "marginRight": 20, "marginTop": 4},
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
        html.Div(
            children="© NewsFlow 2023, Author: Shu-Hao (Ken) Wu",
            style={"text-align": "center", "marginBottom": 20},
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
def update_page(n_clicks, searchVal, countryVal):
    # if n_clicks is None or (searchVal is None or searchVal.strip() == ""):
    #     raise dash.exceptions.PreventUpdate

    new_title, articles_exist = outline.set_vars(countryVal, searchVal)
    if articles_exist:
        top = outline.top
        news_articles = []
        for index, article in enumerate(top["articles"]):
            news_articles.append(
                dbc.AccordionItem(
                    outline.generate_card(index),
                    title=top["articles"][index]["title"],
                    item_id="item-{}".format(index),
                )
            )

        chart_figure = outline.generate_chart(top)
    # If no articles, return an empty list and a message
    else:
        news_articles = [
            html.Div(
                "No articles found. Please try a different search or check your filters.",
                style={"textAlign": "center", "marginTop": "2rem"},
            )
        ]
        chart_figure = {}

    return news_articles, new_title, chart_figure


if __name__ == "__main__":
    # host="0.0.0.0", port="8050"
    app.run_server(debug=False, host="0.0.0.0", port="8050")
    # app.run_server()
