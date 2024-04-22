# Import dependencies
from dash import Dash, html, dcc, Input, Output 
import pandas as pd
import plotly.express as px
import dash
import pandas as pd
df2 = pd.read_csv('data/clean_data.csv')

# Load the CSS stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(style={'backgroundColor': '#white'}, children=[
    html.H1("Book Bestsellers from 2009-2019", style={'text-align': 'center', 'font-family': 'Brush Script MT, cursive', 'font-size': '60px', 'backgroundColor': 'f2f2f2'}),
    
    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'margin-bottom': '20px'}, children=[
        html.Div([
            html.Div([
                html.Img(src='/assets/book1.jpg', style={'width': '150px', 'margin': 'auto', 'display': 'block'}),
            ], style={'width': '10%', 'display': 'inline-block', 'margin-bottom': '60px'}),
            html.Div([
                html.Img(src='/assets/book2.jpg', style={'width': '150px', 'margin': 'auto', 'display': 'block'}),
            ], style={'width': '10%', 'display': 'inline-block', 'margin-bottom': '60px'}),
            html.Div([
                html.Img(src='/assets/book3.jpg', style={'width': '150px', 'margin': 'auto', 'display': 'block'}),
            ], style={'width': '10%', 'display': 'inline-block', 'margin-bottom': '60px'}),
            html.Div([
                html.Img(src='/assets/book4.jpg', style={'width': '150px', 'margin': 'auto', 'display': 'block'}),
            ], style={'width': '10%', 'display': 'inline-block', 'margin-bottom': '60px'}),
            html.Div([
                html.Img(src='/assets/book5.jpg', style={'width': '150px', 'margin': 'auto', 'display': 'block'}),
            ], style={'width': '10%', 'display': 'inline-block', 'margin-bottom': '60px'}),
            html.Div([
                html.Img(src='/assets/book6.jpg', style={'width': '150px', 'margin': 'auto', 'display': 'block'}),
            ], style={'width': '10%', 'display': 'inline-block', 'margin-bottom': '60px'}),
        ], style={'text-align': 'center'}),
        
        html.H3("Select the year(s) and genre(s) of the bestsellers and view the number of books in different price ranges as well as the correlation between user ratings and the number of ratings.", style={'font-family': 'Arial, sans-serif'}),
        
        html.Label("Select Year Range:", style={'font-family': 'Arial, sans-serif', 'font-weight': 'bold'}),
        dcc.RangeSlider(
            id='year-slider',
            min=df2['Year'].min(),
            max=df2['Year'].max(),
            value=[df2['Year'].min(), df2['Year'].max()],
            marks={str(year): str(year) for year in range(df2['Year'].min(), df2['Year'].max() + 1)}
        ),
        
        html.Div([
            html.Div([
                html.Label("Filter by Book Type:", style={'font-family': 'Arial, sans-serif', 'font-weight': 'bold'}),
                dcc.Checklist(
                    id='book-type',
                    options=[
                        {'label': 'Fiction', 'value': 'fiction'},
                        {'label': 'Non-Fiction', 'value': 'non-fiction'}
                    ],
                    value=['fiction', 'non-fiction'],
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'width': '48%', 'display': 'inline-block', 'margin-bottom': '0px'}),
        ]),
    ]),
    
    html.Div([
        html.Div([
            dcc.Graph(id='bar-chart', style={'width': '100%', 'display': 'inline-block'}),
        ], style={'width': '33.33%', 'display': 'inline-block', 'margin-top': '5px'}),
        html.Div([
            dcc.Graph(id='scatter-plot', style={'width': '100%', 'display': 'inline-block'}),
        ], style={'width': '33.33%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='line-chart', style={'width': '100%', 'display': 'inline-block'}),
        ], style={'width': '33.33%', 'display': 'inline-block'})
    ]),
    
    html.Div(style={'backgroundColor': '#white', 'padding': '20px', 'margin-top': '60px'}, children=[
        html.H2("Top 10 Bestsellers", style={'font-family': 'Arial, sans-serif', 'text-align': 'center'}),
        html.Table(id='top-10-table', 
                   style={'width': '50%', 'margin': 'auto', 'font-size': '14px', 'border': '#red'})
    ])
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('line-chart', 'figure'),
     Output('top-10-table', 'children')],
    [Input('year-slider', 'value'),
     Input('book-type', 'value')]
)
def update_charts(year_range, book_type):
    filtered_df = df2[(df2['Year'] >= year_range[0]) & (df2['Year'] <= year_range[1])]
    
    if not book_type:
        return {}, {}, {}, []
    
    if 'fiction' in book_type and 'non-fiction' in book_type:
        pass
    elif 'fiction' in book_type:
        filtered_df = filtered_df[filtered_df['Fiction'] == 1]
    elif 'non-fiction' in book_type:
        filtered_df = filtered_df[filtered_df['Fiction'] == 0]
    else:
        filtered_df = pd.DataFrame()
    
    price_ranges = ['0-10', '11-20', '21-30', '31-40', '41-50', '51+']
    book_counts = []

    for price_range in price_ranges:
        if price_range == '51+':
            count = filtered_df[(filtered_df['Price'] >= 51)].shape[0]
        else:
            price_range_values = price_range.split('-')
            count = filtered_df[(filtered_df['Price'] >= int(price_range_values[0])) &
                                (filtered_df['Price'] <= int(price_range_values[1]))].shape[0]
        book_counts.append(count)

    bar_fig = {
        'data': [{
            'x': price_ranges,
            'y': book_counts,
            'type': 'bar',
            'marker': {
                'color': '#990f02' 
            }
        }],
        'layout': {
            'xaxis': {'title': 'Price Range'},
            'yaxis': {'title': 'Number of Books'},
            'title': 'Number of Books in Different Price Ranges'
        }
    }

    scatter_fig = {
        'data': [{
            'x': filtered_df['Reviews'],
            'y': filtered_df['User Rating'],
            'text': filtered_df['Name'],
            'mode': 'markers',
            'marker': {
                'size': 10,
                'opacity': 0.8,
                'color': '#990f02'
            }
        }],
        'layout': {
            'xaxis': {'title': 'Number of Reviews'},
            'yaxis': {'title': 'User Rating'},
            'title': 'Book Ratings vs Number of Reviews'
        }
    }

    line_fig = {
        'data': [
            {'x': filtered_df[filtered_df['Fiction'] == 1].groupby('Year')['Reviews'].sum().index,
             'y': filtered_df[filtered_df['Fiction'] == 1].groupby('Year')['Reviews'].sum().values,
             'type': 'line',
             'name': 'Fiction',
             'marker': {
                 'color': '#800020'
             }},
            {'x': filtered_df[filtered_df['Fiction'] == 0].groupby('Year')['Reviews'].sum().index,
             'y': filtered_df[filtered_df['Fiction'] == 0].groupby('Year')['Reviews'].sum().values,
             'type': 'line',
             'name': 'Non-Fiction',
             'marker': {
                 'color': '#FF2400'
             }}
        ],
        'layout': {
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Number of Reviews'},
            'title': 'Number of Reviews by Year',
            'legend': {'orientation': 'v'}
        }
    }
    
    top_10_df = filtered_df.groupby('Name')['Reviews'].sum().nlargest(10).reset_index()
    top_10_table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in top_10_df.columns])),
        html.Tbody([
            html.Tr([html.Td(top_10_df.iloc[i][col]) for col in top_10_df.columns], style={'border': '#990f02'}) for i in range(len(top_10_df))
        ])
    ], style={'width': '100%', 'margin': 'auto', 'font-size': '20px', 'border': '#990f02', 'font-family': 'Arial, sans-serif'})
    

    return bar_fig, scatter_fig, line_fig, top_10_table

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
