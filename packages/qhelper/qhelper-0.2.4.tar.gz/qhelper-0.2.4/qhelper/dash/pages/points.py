from dash import callback, dcc, html, Input, Output, register_page
import plotly.express as px
import pandas as pd

register_page(__name__)

# 假设你有一个包含A股所有股票数据的DataFrame
data = {
    '股票代码': ['000001', '000002', '000003', '000004', '000005'],
    '今日成交额': [1000000, 1500000, 2000000, 2500000, 3000000],
    '今日涨跌幅': [0.05, -0.02, 0.03, -0.01, 0.04],
    '市值': [500000000, 800000000, 600000000, 700000000, 650000000],
}

df = pd.DataFrame(data)

# 设置应用布局
layout = html.Div([
    dcc.Graph(id='scatter-plot')  # 定义一个Graph组件
])

@callback(
    Output('scatter-plot', 'figure'),
    [Input('scatter-plot', 'id')]
)
def update_scatter_plot(_):
    fig = px.scatter(
        df,
        x='今日成交额',
        y='今日涨跌幅',
        size='市值',
        color=df['今日涨跌幅'] > 0,  # 根据涨跌幅设置颜色
        color_discrete_map={True: 'red', False: 'green'},
        labels={'color': '涨幅 > 0'},
        title='A股股票今日成交额与涨跌幅散点图',
        hover_name='股票代码',
        size_max=60  # 调整点的最大尺寸
    )
    return fig