import plotly.express as px
import plotly.graph_objects as go


def line_chart(data, title="Stock Price"):

    fig = px.line(
        data,
        x=data.index,
        y='Close',
        title=title
    )

    fig.update_layout(template='plotly_dark')

    return fig


def candlestick_chart(data):

    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])

    fig.update_layout(template='plotly_dark')

    return fig
