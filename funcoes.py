import pandas as pd
import plotly.express as px
from tqdm import tqdm
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt

def plot_candlestick(df_kc,x=None):
    if x is None:
        x=df_kc.index
    fig = go.Figure(data=[go.Candlestick(x=df_kc[x],
                                         open=df_kc['Open'],
                                         high=df_kc['High'],
                                         low=df_kc['Low'],
                                         close=df_kc['Close'],
                                         increasing_line_color='blue',
                                         decreasing_line_color='red',
                                         name='Acão'
                                         )],
                    )
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig


def plot_dataframe(df, title="Preço das açoes"):
    '''
    Retorna um objeto grafico plotly para o pd.dataframe df
    '''
    trace1 = {}
    index = pd.to_datetime(df.index.values)  # .strftime('%Y%m%d-%H:%M')
    for i, k in enumerate(df.columns.to_list()):
        trace1[k] = go.Scatter(x=index,
                               y=df[k].values,
                               name=k)

    fig1 = go.Figure(list(trace1.values()))
    fig1.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center'})

    return fig1


