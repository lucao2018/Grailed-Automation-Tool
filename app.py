import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from Grailed_Bot import Grailed_Bot
from Grailed_Bot import Product_Tracker
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_table
from Grailed_Bot import get_listing_number
from Grailed_Bot import generate_csv

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# set up lists with possible user sizings
bottoms = []
for i in range(26, 45):
    bottoms.append({'label': str(i), 'value': str(i)})

footwear = []
x = 5.0
while x <= 15:
    if x.is_integer():
        x = int(x)
    footwear.append({'label': str(x), 'value': str(x)})
    x += .5

tailoring = []
for i in range(34, 37, 2):
    tailoring.append({'label': str(i) + 'S', 'value': str(i) + 'S'})
    tailoring.append({'label': str(i) + 'R', 'value': str(i) + 'R'})

for i in range(38, 53, 2):
    tailoring.append({'label': str(i) + 'S', 'value': str(i) + 'S'})
    tailoring.append({'label': str(i) + 'R', 'value': str(i) + 'R'})
    tailoring.append({'label': str(i) + 'L', 'value': str(i) + 'L'})

tailoring.append({'label': str(54) + 'R', 'value': str(54) + 'R'})
tailoring.append({'label': str(54) + 'L', 'value': str(54) + 'L'})

accessories = []
accessories.append({'label': "OS", 'value': "OS"})
for i in range(26, 47, 2):
    accessories.append({'label': str(i), 'value': str(i)})

# keep track of listing numbers for tracked products
listingnumber = []

app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[

        dcc.Tab(label='Product search', children=[

            html.Br(),

            html.H2(children="Welcome to the Grailed Automation Tool", style={
                'textAlign': 'center',
            }),
            html.Br(),

            dbc.Row(dbc.Col(html.Div(
                [
                    html.H5(children="Type in the product you want to search for (be as descriptive as possible): "),
                    dcc.Input(id='input-1-state', type='text', value='Product Name')

                ]))),

            html.Br(),
            dbc.Row(dbc.Col(html.Div([
                html.H5(children="Choose the type of product you are searching for: "),
                dcc.Dropdown(
                    id='input-2-state',
                    options=[
                        {'label': 'Tops', 'value': 'Tops'},
                        {'label': 'Bottoms', 'value': 'Bottoms'},
                        {'label': 'Outerwear', 'value': 'Outerwear'},
                        {'label': 'Footwear', 'value': 'Footwear'},
                        {'label': 'Tailoring', 'value': 'Tailoring'},
                        {'label': 'Accessories', 'value': 'Accessories'},
                        {'label': 'None of the above', 'value': 'None of the above'}
                    ],
                    value='Please choose the type of product you are searching for',
                    multi=False
                )]))),

            html.Br(),
            html.Div([
                dbc.Row(dbc.Col(html.Div(html.H5(children="Select sizing that is relevant to your search: ")))),
                dbc.Row([
                    dbc.Col(html.Div([html.H6(children="Tops/outerwear sizing: "),
                                      dcc.Dropdown(
                                          id='input-3-state',
                                          options=[
                                              {'label': 'XXS', 'value': 'XXS/40'},
                                              {'label': 'XS', 'value': 'XS/42'},
                                              {'label': 'S', 'value': 'S44-46'},
                                              {'label': 'M', 'value': 'M48-50'},
                                              {'label': 'L', 'value': 'L/52-54'},
                                              {'label': 'XL', 'value': 'XL/56'},
                                              {'label': 'XXL', 'value': 'XXL/58'}
                                          ],
                                          value='Select your sizing for tops/outerwear',
                                          multi=True
                                      )])),

                    dbc.Col(html.Div([html.H6(children="Bottoms/pants sizing: "),
                                      dcc.Dropdown(
                                          id='input-4-state',
                                          options=bottoms,
                                          value='Select your sizing for pants/bottoms',
                                          multi=True
                                      )])),

                    dbc.Col(html.Div([html.H6(children="Footwear sizing: "),
                                      dcc.Dropdown(
                                          id='input-5-state',
                                          options=footwear,
                                          value='Select your sizing for footwear',
                                          multi=True
                                      )])),
                ])]),

            html.Br(),
            html.Div([
                dbc.Row([
                    dbc.Col(html.Div([html.H6(children="Tailoring sizing: "),
                                      dcc.Dropdown(
                                          id='input-6-state',
                                          options=tailoring,
                                          value='Select your sizing for tailoring',
                                          multi=True
                                      )])),
                    dbc.Col(html.Div([html.H6(children="Accessories sizing: "),
                                      dcc.Dropdown(
                                          id='input-7-state',
                                          options=accessories,
                                          value='Select your sizing for accessories',
                                          multi=True
                                      )]))])]),
            html.Button(id='submit-button', n_clicks=0, children='Submit'),
            html.H5("Here are all of the listings that we found", style={
                'textAlign': 'center',
            }),
            html.Div(id='intermediate-value', style={'display': 'none'}),
            html.Br(),
            html.Div(
                dash_table.DataTable(
                    id='datatable',
                    style_table={'overflowX': 'scroll'},
                    style_cell={
                        'whiteSpace': 'normal'
                    },
                    columns=[{"name": "Product Number", "id": "Product Number"},
                             {"name": "Price ($)", "id": "Price ($)"},
                             {"name": "Shipping Price ($)", "id": "Shipping Price ($)"},
                             {"name": "Total Price ($)", "id": "Total Price ($)"},
                             {"name": "Description", "id": "Description"},
                             {"name": "Seller Rating", "id": "Seller Rating"},
                             {"name": "URL", "id": "URL"}],
                    data=[],
                    css=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],
                    editable=True,
                    sort_action="custom",
                    sort_mode="multi",
                    sort_by=[],
                    row_selectable="multi",
                    row_deletable=True,
                    selected_rows=[],
                    page_action="custom",
                    page_current=0,
                    page_size=15,
                )),
            html.Div(id='output-state'),
            html.Div(dcc.Graph(
                id="datatable-interactivity-container"
            )),
            html.Div([
                html.Pre(id='hover-data')
            ])
        ]),

        dcc.Tab(label="Product Tracking", children=[
            html.Br(),
            html.H4(
                children="Type in the url of a product that you would like to add to your tracking list"),
            dcc.Input(id='input-track-url', type='text', value='Paste the url of the product'),
            html.Button(id='submit-button2', n_clicks=0, children='Submit'),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H6(
                children="Choose up to 10 of the products that you are tracking to see live visualizations of their price"),
            dcc.Dropdown(
                id='products-to-track',
                value='Choose products to visualize',
                multi=True
            ),
            html.Div(id='live-update-graph1'),
            html.Div(id='live-update-graph2'),
            html.Div(id='live-update-graph3'),
            html.Div(id='live-update-graph4'),
            html.Div(id='live-update-graph5'),
            html.Div(id='live-update-graph6'),
            html.Div(id='live-update-graph7'),
            html.Div(id='live-update-graph8'),
            html.Div(id='live-update-graph9'),
            html.Div(id='live-update-graph10'),
            dcc.Interval(
                id='interval-component',
                interval=60000 * 5,
                n_intervals=0
            ),

        ])
    ])
])


@app.callback(Output('intermediate-value', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value'),
               State('input-3-state', 'value'),
               State('input-4-state', 'value'),
               State('input-5-state', 'value'),
               State('input-6-state', 'value'),
               State('input-7-state', 'value')])
def scrape_product(n_clicks, input1, input2, input3, input4, input5, input6, input7):
    if input1 != "Product Name":
        GrailedBot = Grailed_Bot(str(input1), input5, input3, input4, input6, input7, input2)
        GrailedBot.scrape_product()

        return input1

    else:
        raise PreventUpdate


@app.callback(
    Output('datatable', "data"),
    [Input('datatable', "page_current"),
     Input('datatable', "page_size"),
     Input('datatable', "sort_by"), Input('intermediate-value', 'children')])
def update_table(page_current, page_size, sort_by, input1):
    if input1 is None:
        raise PreventUpdate
    else:
        df = pd.read_csv(input1 + '.csv')
        if len(sort_by):
            dff = df.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )
        else:
            dff = df

        return dff.iloc[
               page_current * page_size:(page_current + 1) * page_size
               ].to_dict('records')


@app.callback(
    Output('datatable-interactivity-container', "figure"),
    [Input('datatable', "data"), Input('intermediate-value', 'children')])
def update_graph(rows, input1):
    if input1 is None:
        raise PreventUpdate
    else:
        dff = pd.DataFrame(rows)
        return {
            "data": [
                {
                    "x": dff["Product Number"],
                    "y": dff["Price ($)"],
                    "type": "bar",
                    "marker": {"color": "#7293CB"},
                    "name": "Product Price",
                    'customdata': dff["Product Number"],
                }, {
                    "x": dff["Product Number"],
                    "y": dff["Shipping Price ($)"],
                    "type": "bar",
                    "marker": {"color": "#E1974C"},
                    "name": "Shipping Price",
                    'customdata': dff["Product Number"],
                }
            ],
            "layout": {
                "title": {"text": "Here is a graph of the listings"},
                "xaxis": {"automargin": True,
                          "type": "category",
                          "title": {"text": "Product Number"}},
                "yaxis": {
                    "automargin": True,
                    "title": {"text": "Total Price ($)"}
                },
                "barmode": "stack",
            },
        }


@app.callback(
    Output('hover-data', 'children'),
    [Input('datatable-interactivity-container', 'hoverData'), Input('intermediate-value', 'children')])
def display_hover_data(hoverData, input1):
    if input1 is None:
        raise PreventUpdate
    else:
        if hoverData is not None:
            df = pd.read_csv(input1 + '.csv')
            s = df[df['Product Number'] == hoverData['points'][0]['customdata']]
            return html.H3(
                'Description: {} \n'
                'Seller Rating: {}\n'
                'URL: {}'.format(
                    s.iloc[0]['Description'],
                    s.iloc[0]['Seller Rating'],
                    s.iloc[0]['URL'],
                )
            )


@app.callback(Output('products-to-track', 'options'),
              [Input('submit-button2', 'n_clicks')],
              [State('input-track-url', 'value')])
def add_to_tracking(n_clicks, input1):
    if input1 == "Paste the url of the product":
        raise PreventUpdate
    else:
        generate_csv(get_listing_number(input1))
        listingnumber.append({'label': get_listing_number(input1), 'value': get_listing_number(input1)})
        return listingnumber


@app.callback([Output('live-update-graph1', 'children'),
               Output('live-update-graph2', 'children'),
               Output('live-update-graph3', 'children'),
               Output('live-update-graph4', 'children'),
               Output('live-update-graph5', 'children'),
               Output('live-update-graph6', 'children'),
               Output('live-update-graph7', 'children'),
               Output('live-update-graph8', 'children'),
               Output('live-update-graph9', 'children'),
               Output('live-update-graph10', 'children')],
              [Input('products-to-track', 'value'), Input('interval-component', 'n_intervals')])
def update_price_visualization(input1, n):
    list_of_graphs = []
    if input1 != "Choose products to visualize":
        for listingnumber in input1:
            producttracker = Product_Tracker(listingnumber)
            producttracker.scrape_product()
            df = pd.read_csv(listingnumber + '.csv')

            trace_shipping = go.Scatter(
                x=df['date'],
                y=df['shipping price'],
                name="Shipping price",
                line=dict(color='#E1974C'),
                opacity=0.8)

            trace_price = go.Scatter(
                x=df['date'],
                y=df['price'],
                name="Product Price",
                line=dict(color='#7293CB'),
                opacity=0.8)

            trace_total = go.Scatter(
                x=df['date'],
                y=df['total price'],
                name="Total Price Price",
                line=dict(color='#84BA5B'),
                opacity=0.8)

            data = [trace_price, trace_shipping, trace_total]
            layout = dict(
                title='https://www.grailed.com/listings/' + listingnumber,
                xaxis=dict(
                    title='Date'
                ),
                yaxis=dict(
                    title='$'
                )
            )

            fig = dict(data=data, layout=layout)

            list_of_graphs.append(dcc.Graph(figure=fig))

        while len(list_of_graphs) < 10:
            list_of_graphs.append("Not currently being visualized")

        return list_of_graphs
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
