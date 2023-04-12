from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df_grade = pd.read_csv('YRB_Grade.csv')
df_race = pd.read_csv('YRB_Race.csv')
df_sex = pd.read_csv('YRB_Sex.csv')
df_topic = pd.read_csv('YRB_Topic.csv')
df_sexualOrientation = pd.read_csv('YRB_SexualOrientation.csv')
df_location = pd.read_csv('YRB_Location.csv')

# df = pd.read_csv('DASH_-_Youth_Risk_Behavior_Surveillance_System__YRBSS___High_School____Including_Sexual_Orientation.csv')
fig_grade = px.bar(df_grade, x="Grade", y="Greater_Risk_Data_Value_Avg",
             labels={"Greater_Risk_Data_Value_Avg": "Greater Risk Average"})

fig_race = px.bar(df_race, x="Race", y="Greater_Risk_Data_Value_Avg",
                  labels={"Greater_Risk_Data_Value_Avg": "Greater Risk Average"})

fig_sex = px.bar(df_sex, x="Sex", y="Greater_Risk_Data_Value_Avg",
                  labels={"Greater_Risk_Data_Value_Avg": "Greater Risk Average"})

fig_topic = px.bar(df_topic, x="Topic", y="Greater_Risk_Data_Value_Avg",
                  labels={"Greater_Risk_Data_Value_Avg": "Greater Risk Average"})

fig_sexualOrientation = px.bar(df_sexualOrientation, x="Sexual Orientation", y="Greater_Risk_Data_Value_Avg",
                  labels={"Greater_Risk_Data_Value_Avg": "Greater Risk Average"})

app.layout = html.Div([
    html.Div([
        html.H1(
            "High School Students and Risky Behavior", style={"textAlign": "center"}
        ),
        html.H5(
            "The data shown was collected from a survey of High School students between 2015 and 2017. The data is collected as part of the Youth Risk Behavior Surveillance System (YRBSS).\n"
            "The greater risk behavior value is calculated based on 7 health topics that can be seen in the below graph."
        )
    ]),
    html.Div([
        html.Div([
            html.H3("Risky Behavior Based On Grade Level", style={"textAlign": "center"}),
            dcc.Graph(id='graph_grade',
                figure=fig_grade)
        ], style={'padding': 10, 'flex': 1}),
        html.Div([
            html.Br(),
            html.H4("This dashboard's purpose is to recognize groups of High School students that might be at high risk for risky behvaior. The intention is for you to carefully examine each graph, and determine a way that you can help support the youth in your community"),
            html.Br(),
            html.Ul("The YRBSS was designed to"),
            html.Li("Determine the prevalence of health behaviors."),
            html.Li("Assess whether health behaviors increase, decrease, or stay the same over time."),
            html.Li("Examine the co-occurrence of health behaviors."),
            html.Li("Provide comparable national, state, territorial and freely associated state, tribal, and local data."),
            html.Li("Provide comparable data among subpopulations of youth."),
            html.Li("Monitor progress toward achieving the Healthy People objectives and other program indicators."),
        ], style={'padding': 10, 'flex': 1}),
                html.Div([
            html.H3("Risky Behavior Based On Sex", style={"textAlign": "center"}),
                dcc.Graph(id='graph_sex',
                    figure=fig_sex)
        ], style={'padding': 10, 'flex': 1})        
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    html.Div([
        html.Div([
            html.H3("Risky Behavior Based On Race", style={"textAlign": "center"}),
            dcc.Graph(id='graph_location',
                figure=fig_race)
        ], style={'padding': 10, 'flex': 1}),
        html.Div([
            html.H3("Risky Behavior Based On Question Topic", style={"textAlign": "center"}),
                dcc.Graph(id='graph_topic',
                    figure=fig_topic)
        ], style={'padding': 10, 'flex': 1}),
        html.Div([
            html.H3("Risky Behavior Based On Sexual Identity", style={"textAlign": "center"}),
                dcc.Graph(id='graph_sexualOrientation',
                    figure=fig_sexualOrientation)
        ], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    html.Div([
        html.Div([
            html.H3("Risky Behavior Based On Location", style={"textAlign": "center"}),
            html.Div(
                dcc.Dropdown(
                    id="location-dropdown",
                    multi=True,
                    options=[
                        {"label": x, "value": x}
                        for x in sorted(df_location["LocationDesc"].unique())
                    ],
                    value=["Texas", "United States", "California", "Florida", "Utah"]
                ),
                className="three columns",
            ),
            html.Br(),
            html.Div(
                dcc.Checklist(
                    ['Greater Risk', 'Lesser Risk'],
                    value=['Greater Risk'],
                    id="location_check",
                    labelStyle={'color':'azure'}
                )
            ),
            html.Br(),
            dcc.Graph(id='graph_location')
                # figure=fig_location
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    html.Div(
        html.A(
            id="my-link",
            children="Click here for the dataset",
            href="https://chronicdata.cdc.gov/Youth-Risk-Behaviors/DASH-Youth-Risk-Behavior-Surveillance-System-YRBSS/q6p7-56au",
            target="_blank",
            style={"color": "azure"}
        )
    )
])

@app.callback(
    Output('graph_location', 'figure'),
    [Input('location-dropdown', 'value'),
    Input('location_check', 'value')]
    )
def update_figure(chosen_value, check_value):
    print(f"Values chosen by user: {chosen_value}")
    print(f"Radio Value: {check_value}")



    if len(chosen_value) == 0:
        return {}
    else:
        if check_value == ['Greater Risk']:
            df_filtered = df_location[df_location["LocationDesc"].isin(chosen_value)]
            fig = px.bar(df_filtered,
                x="LocationDesc",
                y="Greater Risk Average")
            fig.update_layout(yaxis_range=[0, 80])
            return fig
        elif check_value == ['Lesser Risk']:
            df_filtered = df_location[df_location["LocationDesc"].isin(chosen_value)]
            fig = px.bar(df_filtered,
                x="LocationDesc",
                y="Lesser Risk Average")
            fig.update_layout(yaxis_range=[0, 80])
            return fig
        elif check_value == (['Greater Risk', 'Lesser Risk'] or ['Lesser Risk', 'Greater Risk']):
            df_filtered = df_location[df_location["LocationDesc"].isin(chosen_value)]
            fig = px.bar(df_filtered,
                x="LocationDesc", 
                y=['Greater Risk Average', 'Lesser Risk Average'],
                barmode= 'group'           
            )
            fig.update_layout(yaxis_range=[0, 80])
            return fig    
        elif check_value == (['Lesser Risk', 'Greater Risk']):
            df_filtered = df_location[df_location["LocationDesc"].isin(chosen_value)]
            fig = px.bar(df_filtered,
                x="LocationDesc", 
                y=['Greater Risk Average', 'Lesser Risk Average'],
                barmode= 'group'
            )
            fig.update_layout(yaxis_range=[0, 80])
            return fig     
        else:
            return {}


if __name__ == '__main__':
    app.run_server(debug=True)