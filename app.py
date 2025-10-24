import dash
from dash import html, dcc
import plotly.express as px
import threading
from sniffing import start_sniffing, get_mac_counts
print(get_mac_counts())

#start sniffing
sniff_thread = threading.Thread(target=start_sniffing, args=('wlan0mon',), daemon=True)
sniff_thread.start()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Wi-Fi Monitoring dashboard"),
    dcc.Graph(id='mac-traffic-graph'),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0)
])

@app.callback(
    dash.dependencies.Output('mac-traffic-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    mac_data = get_mac_counts()
    if not mac_data:
        return px.bar(x=[], y=[], labels={'x': 'MAC Address', 'y': 'Packet Count'})
    
    macs = list(mac_data.keys())
    counts = list(mac_data.values())
    fig = px.bar(x=macs, y=counts, labels={'x': 'MAC Address', 'y': 'Packet Count'})
    return fig

if __name__ == '__main__':
    app.run(debug=True)