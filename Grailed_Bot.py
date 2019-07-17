import csv
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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID], )
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
listingnumber = []


def get_listing_number(url):
    listingnumber = ""
    index = 0

    for i in range(0, len(url)):
        if url[i].isdigit():
            index = i
            break

    print(index)

    for i in range(index, len(url)):
        if url[i].isdigit():
            listingnumber += url[i]
        else:
            break

    return listingnumber


def generate_csv(listingnumber):
    with open(listingnumber + '.csv', 'w', newline='', encoding='utf-8') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(
            ['date', 'price', 'shipping price', 'total price', 'description', 'user rating'])


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
            html.H6("Here are all of the listings that we found", style={
                'textAlign': 'center',
            }),
            html.Br(),
            html.Div(id='output-state'),
            html.Div(id='hover-info'),
            html.Div(id='output-state2')
        ]),

        dcc.Tab(label="Product Tracking", children=[
            html.H6(
                children="Type in the url of a product that you would like to add to your tracking list"),
            dcc.Input(id='input-track-url', type='text', value='Paste the url of the product'),
            html.Button(id='submit-button2', n_clicks=0, children='Submit'),
            html.H6("Here is a line graph that will track the price of the product over time: "),
            html.H6(
                children="Choose up to 10 of the products that you are tracking to see visualization of price"),
            html.Div(id='products-to-track-test'),

            dcc.Dropdown(
                id='products-to-track',
                # options=listingnumber,
                value='Choose products to visualize',
                multi=True
            ),
            # html.Button(id='submit-button3', n_clicks=0, children='Submit'),
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
                interval=60000 * 5,  # in milliseconds
                n_intervals=0
            ),

        ])
    ])
])


@app.callback([Output('output-state', 'children'),
               Output('output-state2', 'children')],
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value'),
               State('input-3-state', 'value'),
               State('input-4-state', 'value'),
               State('input-5-state', 'value'),
               State('input-6-state', 'value'),
               State('input-7-state', 'value')])


def multi_output(n_clicks, input1, input2, input3, input4, input5, input6, input7):
    if input1 != "Product Name":
        GrailedBot = Grailed_Bot(str(input1), input5, input3, input4, input6, input7, input2)
        GrailedBot.scrape_product()
        print("made it here")
        df = pd.read_csv(input1 + '.csv')
        table = generate_table(df)
        graph = generate_stacked_chart(input1 + '.csv')

        return table, graph
    else:
        raise PreventUpdate


def generate_table(dataframe, max_rows=10, ):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


def generate_stacked_chart(csvname):
    shipping_costs = []
    product_price = []
    product_number = []
    urls = []
    hovertext = []
    with open(csvname, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            shipping_costs.append(line[2])
            product_price.append(line[1])
            urls.append(line[6])
            product_number.append(line[0])
            hovertext.append("Shipping Price: $" + line[2] + "<br>" +
                             "Total Price with shipping: $" + line[3] + "<br>" "Seller rating: " + line[
                                 5] + "<br>" + "Url: " + line[6])

    trace1 = go.Bar(
        x=product_number,
        y=product_price,
        name='Product Price',
        hovertemplate='Price : $%{y:.2f}'
                      '<br>%{text}',
        text=hovertext
    )

    trace2 = go.Bar(
        x=product_number,
        y=shipping_costs,
        name="Shipping Costs"
    )

    return dcc.Graph(
        id='stacked_total_cost_bar_chart',
        figure=go.Figure(data=[trace1, trace2],
                         layout=go.Layout(barmode='stack', title="Stacked Bar Chart of Listing Costs",
                                          xaxis=go.layout.XAxis(
                                              title=go.layout.xaxis.Title(
                                                  text='Product Number'
                                              )
                                          ),

                                          yaxis=go.layout.YAxis(
                                              title=go.layout.yaxis.Title(
                                                  text='Price $(USD)'
                                              )
                                          )
                                          )
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
    print(input1)
    list_of_graphs = []
    if input1 != "Choose products to visualize":
        for listingnumber in input1:
            producttracker = Product_Tracker(listingnumber)
            producttracker.scrape_product()
            df = pd.read_csv(listingnumber + '.csv')
            print("made it here")
            trace_shipping = go.Scatter(
                x=df['date'],
                y=df['shipping price'],
                name="shipping price",
                line=dict(color='#17BECF'),
                opacity=0.8)

            trace_price = go.Scatter(
                x=df['date'],
                y=df['price'],
                name="Product Price",
                line=dict(color='#7F7F7F'),
                opacity=0.8)

            trace_total = go.Scatter(
                x=df['date'],
                y=df['total price'],
                name="Total Price Price",
                line=dict(color='#7F7F7F'),
                opacity=0.8)

            data = [trace_price, trace_shipping, trace_total]
            layout = dict(
                title=listingnumber,
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
