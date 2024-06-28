from dash import Dash, html, dcc, page_registry, page_container
import plotly.graph_objs as go

def create_dash_app(server):
    # 创建 Dash 应用
    app = Dash(__name__, server=server, url_base_pathname='/dash/', use_pages=True)

    app.layout = html.Div([
        html.H1('Multi-page app with Dash Pages'),
        html.Div([
            html.Div(
                dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
            ) for page in page_registry.values()
        ]),
        page_container
    ])

    return app
