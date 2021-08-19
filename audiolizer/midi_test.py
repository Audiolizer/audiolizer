# -*- coding: utf-8 -*-
# built on webaudiofont https://surikov.github.io/webaudiofont/

# %load_ext autoreload
# %autoreload 2

from midi_loader import instruments, instrument_paths, instrument_pitches

from jupyter_dash import JupyterDash

from dash import Dash

from dash.dependencies import Input, Output, ClientsideFunction

from dash.exceptions import PreventUpdate

import json

# +
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = JupyterDash(__name__,
                  external_stylesheets=external_stylesheets,
                  external_scripts=['https://surikov.github.io/webaudiofont/npm/dist/WebAudioFontPlayer.js',
                                    'https://surikov.github.io/webaudiofontdata/sound/0250_SoundBlasterOld_sf2.js',
                                    'https://surikov.github.io/webaudiofontdata/sound/0240_Chaos_sf2_file.js',])

base = 'https://surikov.github.io/webaudiofontdata/sound/'

cat_0 = list(instruments.keys())[0]
instr_type_0 = list(instruments[cat_0].keys())[0]
instr_0 = instruments[cat_0][instr_type_0][0]

simple_pitch = html.Div(children=[
    html.Div(html.A(href='https://surikov.github.io/webaudiofont/', children='webaudiofont')),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='category',
                options=[{'label': cat, 'value': cat} for cat in instruments.keys()],
                value=cat_0,
                clearable=False),
            dcc.Dropdown(
                id='instrument-type',
                options=[{'label': instr, 'value': instr} for instr in instruments[cat_0]],
                value=instr_type_0,
                clearable=False),
            dcc.Dropdown(
                id='preset',
                options=[dict(label=_, value=_) for _ in instruments[cat_0][instr_type_0]],
                value=instr_0,
                clearable=False),
            html.Div(id='path', children='hey'),
        ], className='three columns'),
        html.Div([
            html.Div('pitches'),
            dcc.RangeSlider(id='pitches', min=0, max=127,
                    value=[40, 50, 60, 70, 80, 90]),
            ], className='two columns'),
        html.Div([
            html.Div('duration'),
            dcc.Input(id='duration', min=0, value=2, type='number')
            ], className='two columns'),
        html.Div([
            html.Div('volume'),
            dcc.Input(id='volume', min=0, value=1, type='number', step=.1),
            ], className='two columns'),
        html.Div([html.Br(), html.Button('stop', id='stop', n_clicks=0)], className='two columns'),
        ], className='row'),
    dcc.Store(id='midi-data'),
    html.Div(id='out-component', children='True'),
    html.Div(id='out-component2', children='True'),
    html.Div(id='stop-clicks', children=''),
    ])


# audioContext - AudioContext
# target - a node to connect to, for example audioContext.destination
# preset - variable with the instrument preset
# when - when to play, audioContext.currentTime or 0 to play now, audioContext.currentTime + 3 to play after 3 seconds
# pitch - note pitch from 0 to 127, for example 2+12*4 to play D of fourth octave (use MIDI key for drums)
# duration - note duration in seconds, for example 4 to play 4 seconds
# volume - 0.0 <=1.0 volume (0 is ‘no value’, ‘no value’ is 1)
# slides - array of pitch bends

# queueWaveTable(audioContext, target, preset, when, pitch, duration, volume, slides)

@app.callback(
    Output('instrument-type', 'options'),
    Output('instrument-type', 'value'),
    Input('category', 'value'))
def fetch_instrument_types(cat):
    instrument_types_ = list(instruments[cat].keys())
    return [dict(label=_, value=_) for _ in instrument_types_], instrument_types_[0]

@app.callback(
    Output('preset', 'options'),
    Output('preset', 'value'),
    Input('category', 'value'),
    Input('instrument-type', 'value'))
def fetch_instruments(cat, instrument_type):
    instruments_ = list(instruments[cat][instrument_type])
    first_inst = instruments_[0]
    return [dict(label=_, value=_) for _ in instruments_], first_inst

@app.callback(
    Output('path', 'children'),
    Input('preset', 'value'))
def fetch_instrument_path(instrument_name):
    return instrument_paths[instrument_name]

# @app.callback(
#     Output('pitch', 'value'),
#     Input('preset', 'value'))
# def fetch_instrument_pitch(instrument_name):
#     pitch = instrument_pitches.get(instrument_name)
#     if pitch is not None:
#         return int(instrument_pitches[instrument_name])
#     raise PreventUpdate

@app.callback(
    Output('midi-data', 'data'),
    Input('pitches', 'value'),
    Input('duration', 'value'),
    Input('volume', 'value'))
def send_notes(pitches, dur, vol):
    when = []
    duration = []
    volume = []
    for i, pitch in enumerate(pitches):
        when.append(i)
        duration.append(dur)
        volume.append(vol)
    notes = dict(when=when, pitch=pitches, duration=duration, volume=volume)
    return notes


app.clientside_callback(
    ClientsideFunction(namespace='dash_midi', function_name='play'),
    Output('out-component', 'children'),
    Input('preset', 'value'),
    Input('path', 'children'),
    Input('midi-data', 'data'))

app.clientside_callback(
    ClientsideFunction(namespace='dash_midi', function_name='stop'),
    Output('stop-clicks', 'children'),
    Input('stop', 'n_clicks'))



app.layout = html.Div([simple_pitch])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',
                   port=8051,
                   mode='external',
                   debug=True)
# -

