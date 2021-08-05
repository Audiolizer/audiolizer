from jupyter_dash import JupyterDash

from dash import Dash

from dash.dependencies import Input, Output

# +
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = JupyterDash(__name__,
                  external_stylesheets=external_stylesheets,
                  external_scripts=['https://surikov.github.io/webaudiofont/npm/dist/WebAudioFontPlayer.js',
                                    'https://surikov.github.io/webaudiofontdata/sound/0250_SoundBlasterOld_sf2.js'])


app.layout = html.Div(children=[
    dcc.Input(id='in-component1', value=12, type='number'),
    dcc.Input(id='duration', value=2, type='number'),
    html.Div(id='out-component')

])

app.clientside_callback(
    """
    function play(input1, duration){
        player.queueWaveTable(audioContext, audioContext.destination
            , _tone_0250_SoundBlasterOld_sf2, 0, parseInt(input1), duration);
        return false;
    }
    """,
    Output('out-component', 'children'),
    Input('in-component1', 'value'),
    Input('duration', 'value')
)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, mode='external', debug=True)
# -

