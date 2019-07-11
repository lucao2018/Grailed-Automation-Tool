import csv
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from Grailed_Bot import Grailed_Bot
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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

app.layout = html.Div([
    html.H4(children="Welcome to the Grailed Automation Tool"),
    html.H6(children="Type in the product you want to search for: "),
    dcc.Input(id='input-1-state', type='text', value='Product Name (be as descriptive as possible)'),
    html.H6(children="Choose the type of product you want to search for"),
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
    ),
    html.H6(children="Select sizing that is relevant to your search query: "),
    html.H6(children="Tops/outerwear sizing: "),
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
    ),
    html.H6(children="Bottoms/pants sizing: "),
    dcc.Dropdown(
        id='input-4-state',
        options=bottoms,
        value='Select your sizing for pants/bottoms',
        multi=True
    ),
    html.H6(children="Footwear sizing: "),
    dcc.Dropdown(
        id='input-5-state',
        options=footwear,
        value='Select your sizing for footwear',
        multi=True
    ),
    html.H6(children="Tailoring sizing: "),
    dcc.Dropdown(
        id='input-6-state',
        options=tailoring,
        value='Select your sizing for tailoring',
        multi=True
    ),
    html.H6(children="Accessories sizing: "),
    dcc.Dropdown(
        id='input-7-state',
        options=accessories,
        value='Select your sizing for accessories',
        multi=True
    ),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.H6("Here are all of the listings that we found"),
    html.Div(id='output-state'),
    html.H6("Here is a stacked bar chart of all of the listing costs"),
    html.Div(id='hover-info'),
    html.Div(id='output-state2')
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
    if input1 != "Product Name (be as descriptive as possible)":
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
                         layout=go.Layout(barmode='stack',
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


if __name__ == '__main__':
    app.run_server(debug=True)
