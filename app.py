import dash
from dash import html,dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc 
from dash_bootstrap_templates import load_figure_template

load_figure_template("minty")



app = dash.Dash(
    external_stylesheets=[dbc.themes.MINTY,'https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap',]
)
server = app.server


df_data = pd.read_csv("supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data["Date"])

df_data["City"].value_counts().index





# ====================  Layout  ========================= #
app.layout = html.Div(children=[

    
    dbc.Row([
        dbc.Col([
                dbc.Card([   
                    html.H1("JHENERSON ROSARIO",style={'font-family':'Bebas Neue','font-size':'35px','font-weight':'400','font-style':'normal','color':'Black'}),
                    html.Hr(),             
                    html.H5("Cities"),
                    dcc.Checklist(df_data["City"].value_counts().index, df_data["City"].value_counts().index, id="check_city", inputStyle={"margin":"5px"}),
                    html.H5("Analysis Variable", style={"margin-top": "10px"}),
                    dcc.RadioItems(["gross income", "Rating"], "gross income", id="main_variable"),
                    ],style={"height":"90vh","margin":"20px", "padding":"20px",}),

                 ],sm=2,),
        
        dbc.Col([
                    dbc.Row([dbc.Col([dcc.Graph(id="city_fig")],sm=4),
                             dbc.Col([dcc.Graph(id="gender_fig")],sm=4),
                             dbc.Col([dcc.Graph(id="pay_fig")],sm=4),
                             
                             
                             ]),
                    dbc.Row([dcc.Graph(id="income_per_date_fig")]),
                    dbc.Row([dcc.Graph(id="income_per_products_fig")]),
                    


                 ],sm=10)
    ])
])




# ===================  Callbacks  ================= #
@app.callback([
                Output('city_fig', 'figure'),
                Output('pay_fig', 'figure'),
                Output('gender_fig', 'figure'),
                Output('income_per_products_fig', 'figure'),
                Output('income_per_date_fig', 'figure')
            ],
              [
                  Input('check_city', 'value'),
                  Input('main_variable', 'value')
              ])

def render_gaphs(cities, main_variable):
    operation = np.sum if main_variable == "gross income" else np.mean

    df_filtered = df_data[df_data["City"].isin(cities)]

    df_city = df_filtered.groupby("City")[main_variable].apply(operation).to_frame().reset_index()
    df_gender = df_filtered.groupby(["Gender","City"])[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(operation).to_frame().reset_index()
    df_product_date_income = df_filtered.groupby("Date")[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(["Product line","City"])[main_variable].apply(operation).to_frame().reset_index()

    fig_city = px.bar(df_city, x="City", y=main_variable,color="City", color_discrete_map={'Mandalay':'#1C87D7'})
    fig_payment = px.bar(df_payment, x=main_variable, y="Payment", orientation="h",color="Payment", color_discrete_map={'Cash':'#1C87D7'})
    fig_gender = px.bar(df_gender, y=main_variable,x="Gender" ,color="City", barmode="group",color_discrete_map={'Mandalay':'#1C87D7'})
    fig_product_income = px.bar(df_product_income, x=main_variable, y="Product line", color="City", orientation="h", barmode='group',color_discrete_map={'Mandalay':'#1C87D7'})
    fig_income_date = px.bar(df_product_date_income, y=main_variable, x="Date")

    for fig in [fig_city,fig_payment,fig_gender, fig_income_date]:
   
        fig.update_layout(margin=dict(l=0, t=20, b=20), height=200, template="minty")
    
    fig_product_income.update_layout(margin=dict(l=0, t=20, b=20), height=500, )

    return fig_city, fig_payment,fig_gender ,fig_product_income, fig_income_date








# ============= Run Server ======================== #

if __name__ == "__main__":
    app.run_server(port=8050, debug=False)