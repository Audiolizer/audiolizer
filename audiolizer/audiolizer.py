
import logging
import os
import time
from collections import defaultdict
from datetime import datetime

import dash
import dash.dcc as dcc
from dash import html
import numpy as np
import pandas as pd
from dash.dependencies import ClientsideFunction, Input, Output, State
from dash.exceptions import PreventUpdate
from flask import Flask, redirect, url_for, request, jsonify
from flask_dance.contrib.google import google, make_google_blueprint
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo.errors import DuplicateKeyError

from history import get_granularity, get_history, get_today_GMT
from db import users, ph, authenticate_user
from convert import get_scale_notes, merge_pitches, freq_to_degrees, pitch_from_freq, freq_from_pitch, frequency_marks, midi_note, clear_files, candlestick_plot, refactor
from psidash.psidash import assign_callbacks, get_callbacks, load_app, load_components, load_conf, load_dash
from Historic_Crypto import Cryptocurrencies



# Configuration and logger setup
logging.basicConfig(filename='audiolizer.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Crypto data
data = Cryptocurrencies(coin_search='', extended_output=True).find_crypto_pairs()
crypto_dict = {}
for base, group in data.groupby('base_currency'):
    crypto_dict[base] = list(group.quote_currency.unique())

# Environment variables and thresholds
audiolizer_temp_dir = os.environ.get('AUDIOLIZER_TEMP', './history/')
logger.info('audiolizer temp data:{}'.format(audiolizer_temp_dir))
granularity = int(os.environ.get('AUDIOLIZER_GRANULARITY', 300))  # seconds
wav_threshold = int(os.environ.get('AUDIOLIZER_WAV_CACHE_SIZE', 100))  # megabytes
midi_threshold = int(os.environ.get('AUDIOLIZER_MIDI_CACHE_SIZE', 10))
price_threshold = int(os.environ.get('AUDIOLIZER_PRICE_CACHE_SIZE', 100))
enable_user_logins = os.environ.get('ENABLE_USER_LOGINS', '').lower() == 'true'
enable_google_logins = os.environ.get('ENABLE_GOOGLE_LOGINS', '').lower() == 'true'

logger.info('cache sizes: \n wav:{}Mb\n midi:{}Mb\n price:{}Mb'.format(wav_threshold, midi_threshold, price_threshold))



conf = load_conf('../audiolizer.yaml')

app = load_dash(__name__, conf['app'], conf.get('import'))

app.server.config.update(
    SECRET_KEY=os.environ.get('APP_SECRET'),
)


login_manager = LoginManager()
login_manager.init_app(app.server)
login_manager.login_view = '/'

class User(UserMixin):
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_id(self):
        return self.username

    @staticmethod
    def get(username):
        user_data = users.find_one({"username": username})
        if user_data:
            return User(username=user_data['username'], email=user_data['email'])
        return None

@login_manager.user_loader
def load_user(username):
    return User.get(username)


@app.server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')



@app.callback(
    Output('url', 'pathname'),
    [Input('url', 'pathname'), Input('logout-button', 'n_clicks')]
)
def handle_authentication(pathname, logout_clicks):
    if logout_clicks:
        logout_user()
        return '/'
    
    if enable_user_logins:
        if enable_google_logins:
            if not (google.authorized or current_user.is_authenticated):
                return '/'
        else:
            if current_user.is_authenticated:
                return '/'

    return dash.no_update


if enable_google_logins:
    google_bp = make_google_blueprint(
        client_id=os.environ['GOOGLE_CLIENT_ID'],
        client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
        scope=["openid"],
        redirect_to='/'
    )

    app.server.register_blueprint(google_bp, url_prefix="/login")

    @app.server.route('/login/google')
    def google_login():
        print("Attempting to redirect to Google login.")
        return flask.redirect(flask.url_for('google.login'))

    # Assuming `app.server` is your Flask server instance
    @app.server.route('/login/google/authorized')
    def google_authorized():
        # This function should handle the OAuth callback logic
        # Redirect to the root of your Dash app after login
        return flask.redirect('/')



initial_layout = load_components(conf['layout'], conf.get('import'))
login_layout = load_components(conf['login_layout'], conf.get('import'))

if enable_google_logins:
    login_google = load_components(conf['login_google'], conf.get('import'))
    login_layout.children.append(login_google)


main_layout = load_components(conf['main_layout'], conf.get('import'))


app.layout = initial_layout


if 'callbacks' in conf:
    callbacks = get_callbacks(app, conf['callbacks'])
    assign_callbacks(callbacks, conf['callbacks'])



@callbacks.display_layout
def display_layout(pathname):
    if enable_user_logins:
        if enable_google_logins:
            if google.authorized or current_user.is_authenticated:
                return main_layout
        elif current_user.is_authenticated: 
                return main_layout
        else:
            return login_layout
    else:
        return main_layout

scale_modes = conf['scale_modes']

def beeper(freq, amplitude=1, duration=.25):
    return (amplitude*_ for _ in audiogen_p3.beep(freq, duration))

def get_frequency(price, min_price, max_price, log_frequency_range):
    """linear map from price to frequency"""
    return np.interp(price, [min_price, max_price], [10**_ for _ in log_frequency_range])

@callbacks.update_base_options
def update_base_options(url):
    return [{'label': base, 'value': base} for base in crypto_dict]

@callbacks.update_quote_options
def update_quote_options(base, quote_prev):
    quotes = crypto_dict[base]
    options = [{'label': quote, 'value': quote} for quote in quotes]
    if quote_prev in quotes:
        quote = quote_prev
    else:
        quote = quotes[0]
    return quote, options

@callbacks.slider_marks
def update_marks(url):
    return frequency_marks

@callbacks.update_date_range
def update_date_range(date_select):
    period, cadence = date_select.split('-')
    today = get_today_GMT().tz_localize('GMT') #.tz_convert(timezone)
    logger.info('Period was {}'.format(period))
    start_date = (today-pd.Timedelta(period)).strftime('%Y-%m-%d')
#     end_date = (today+pd.Timedelta('1d')).strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')

    date_range_start = start_date
    date_range_end = end_date
    initial_visible_month = start_date
    return date_range_start, date_range_end, cadence, initial_visible_month


@app.callback(
    Output('login-status', 'children'),
    [Input('manual-login-btn', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def manual_login(n_clicks, username, password):
    if n_clicks:
        if authenticate_user(username, password):
            user = User.get(username)
            login_user(user)
            return dcc.Location(href='/', id='redirect')
        else:
            return html.Div('Invalid credentials', style={'color': 'red'})
    return ''


@app.callback(
    Output('nav-username', 'children'),
    [Input('url', 'pathname')]
)
def update_nav_username(pathname):
    if enable_user_logins:
        if current_user.is_authenticated:
            return html.Span(f"Logged in as: {current_user.username}")
        elif enable_google_logins:
            if google.authorized:
                resp = google.get("/oauth2/v3/userinfo")
                assert resp.ok, resp.text
                user_info = resp.json()
                return html.Span(f"Logged in as: {user_info}")
    return html.Span("Not logged in")



@callbacks.play
def play(base, quote,
         start, end,
         cadence,
         tonic,
         semitone_sequence,
         log_freq_range,
         # drop_quantile, beat_quantile,
         tempo,
         toggle_merge,
         # silence,
         # selectedData,
         price_type,
         ):

    if len(price_type) == 0:
        raise PreventUpdate

    t0 = time.perf_counter()
    # logger.info('timezone = {}'.format(timezone))
    ticker = '{}-{}'.format(base, quote)
    logger.info('ticker: {}'.format(ticker))
    
    # clear extraneous midi files
    cleared = clear_files('assets/*.midi', max_storage=midi_threshold*1e6)
    if len(cleared) > 0:
        logger.info('cleared {} midi files'.format(len(cleared)))
        
    t1 = time.perf_counter()
    logger.info('time to clear midi {}'.format(t1-t0))
    t0 = t1
    
    # clear extraneous history files
    cleared = clear_files('history/*.csv.gz', max_storage=price_threshold*1e6)
    if len(cleared) > 0:
        logger.info('cleared {} price files'.format(len(cleared)))

    t1 = time.perf_counter()
    logger.info('time to clear price {}'.format(t1-t0))
    t0 = t1

    logger.info('start, end {} {}'.format(start, end))
    granularity = get_granularity(cadence)
    
    
    t1 = time.perf_counter()
    logger.info('time to init play {}'.format(t1-t0))
    t0 = t1
    
    try:
        new = get_history(ticker, granularity, start, end)
    except:
        logger.info('cannot get history for {} {} {}'.format(ticker, start, end))
        raise
    
    t1 = time.perf_counter()
    logger.info('time to get history {}'.format(t1-t0))
    t0 = t1
    
    start_, end_ = new.index[[0, -1]]

    if (end_-start_).days == 1:
        # make sure we get exactly 24 hrs of data
        logger.info('make sure we get exactly 24 hrs of data')
        start_ = end_ - pd.Timedelta('1d')

    if toggle_merge:
        merged = 'merged'
    else:
        merged = ''
    # if silence:
    #     silences = 'rests'
    # else:
    #     silences = ''

    scale_notes = get_scale_notes(tonic, semitone_sequence)

    mode_label = next((item['label'] for item in scale_modes if item['value'] == semitone_sequence), 'unknown')

    fname = '{}_{}_{}_{}_{}_{}_{}_{}_{}.wav'.format(
        ticker,
        '-'.join(price_type),
        start_.date(),
        end_.date(),
        cadence,
        tonic.replace('#', 'sharp'),
        mode_label.replace(' ', ''),
        # drop_quantile,
        # beat_quantile,
        '{}bpm'.format(tempo),
        merged,
        # silences,
    )

    midi_file = fname.split('.wav')[0] + '.midi'

    duration = 60./tempo # length of the beat in seconds (tempo in beats per minute)

    t1 = time.perf_counter()
    logger.info('time to set midi params {}'.format(t1-t0))
    t0 = t1

    new_ = refactor(new[start_:end_], cadence)
    logger.info('{}->{}'.format(*new_.index[[0,-1]]))
    
    midi_asset = app.get_asset_url(midi_file)

    max_vol = new_.volume.max() # normalizes peak amplitude
    min_price = new_[price_type].values.ravel().min() # sets lower frequency bound
    max_price = new_[price_type].values.ravel().max() # sets upper frequency bound

    # amp_min = beat_quantile/100 # threshold amplitude to merge beats
    # min_vol = new_.volume.quantile(drop_quantile/100) # threshold volume to silence
    
    
    t1 = time.perf_counter()
    logger.info('time to set up beeps {}'.format(t1-t0))
    t0 = t1

    notes = defaultdict(list)
    max_freq_ = 0
    max_amp_ = 0

    for price_type_ in price_type:
        beeps = []
        for t, (price, volume_) in new_[[price_type_, 'volume']].iterrows():
            if ~np.isnan(price):
                freq_ = get_frequency(price, min_price, max_price, log_freq_range)
                freq_ = freq_from_pitch(pitch_from_freq(freq_, scale_notes))
                beep = t, midi_note(freq_), volume_/max_vol, duration
                beeps.append(beep)
            else:
                freq_ = get_frequency(min_price, min_price, max_price, log_freq_range)
                freq_ = freq_from_pitch(pitch_from_freq(freq_, scale_notes))
                beep = t, midi_note(freq_), 0, duration
                beeps.append(beep)
                logger.warning('found nan price {}, {}, {}'.format(t, price, volume_))

        if toggle_merge:
            beeps = merge_pitches(beeps)

        # if silence:
        #     beeps = quiet(beeps, min_vol/max_vol)
            
        dur0 = 0
        for t, freq_, amp_, dur_ in beeps:
            notes['t'].append(t)
            notes['when'].append(dur0)
            notes['pitch'].append(freq_)
#             notes['duration'].append(duration*(1+3*amp_)) # peak amp will get 4 beats
#             notes['duration'].append(duration*1.5)
            notes['duration'].append(dur_)
            notes['volume'].append(1) # could use a constant amplitude
            max_freq_ = max(max_freq_, freq_)
            max_amp_ = max(max_amp_, amp_)
#             dur0 += duration
            dur0 += dur_
            
#     print('max frequency was {}'.format(max_freq_))
#     print('max amp was {}'.format(max_amp_))

    t1 = time.perf_counter()
    logger.info('time to generate audio {}'.format(t1-t0))
    t0 = t1

    # consider how to generate this in memory
    # write_midi(beeps, tempo, 'assets/' + midi_file)

    t1 = time.perf_counter()
    logger.info('time to write audio data {}'.format(t1-t0))
    t0 = t1
    df = new_.reset_index()

    df['time'] = df['time'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    candlestick_data = df.to_dict()
    candlestick_data['base'] = base
    candlestick_data['quote'] = quote

    # print(json.dumps(candlestick_data))
    

    return (candlestick_data,
            notes,
            # midi_asset,
            # midi_asset,
            '',
            )


app.clientside_callback(
    ClientsideFunction(namespace='dash_midi', function_name='stop'),
    Output('stop-clicks', 'children'),
    Input('stop', 'n_clicks'))

app.clientside_callback(
    ClientsideFunction(namespace='dash_midi', function_name='pause'),
    Output('pause-clicks', 'children'),
    Input('pause', 'n_clicks'))



app.clientside_callback(
    ClientsideFunction(namespace='dash_midi', function_name='play'),
    Output('midi-display', 'children'),
    Input('play', 'n_clicks'),
    State('instrument', 'value'),
    State('preset-path', 'children'),
    State('midi-data', 'data'))


app.clientside_callback(
    ClientsideFunction(namespace='dash_midi', function_name='playFromSelect'),
    Output('on-select-display', 'children'),
    Input('candlestick-chart', 'selectedData'),
    State('instrument', 'value'),
    State('preset-path', 'children'),
    State('midi-data', 'data'))


app.clientside_callback(
    ClientsideFunction(namespace='dash_midi', function_name='playFromClick'),
    Output('on-click-display', 'children'),
    Input('candlestick-chart', 'clickData'),
    State('instrument', 'value'),
    State('preset-path', 'children'),
    State('midi-data', 'data'))

app.clientside_callback(
    ClientsideFunction(namespace='dash_midi', function_name='playOnHover'),
    Output('on-hover-display', 'children'),
    Input('candlestick-chart', 'hoverData'),
    State('instrument', 'value'),
    State('preset-path', 'children'),
    State('midi-data', 'data'))

app.clientside_callback(
    ClientsideFunction(namespace='dash_midi', function_name='updateFigure'),
    Output('candlestick-chart', 'figure'),
    Input('candlestick-data', 'data'),  # Assuming this is a dcc.Store or similar
    Input('timestamp-listener', 'n_events'),
    State('timestamp-listener', 'event')  # The input element where timestamp is stored
)


server = app.server

if __name__ == '__main__':
    app.run_server(
        host=conf['run_server']['host'],
        port=conf['run_server']['port'],
        debug=True,
        dev_tools_hot_reload=False,
        extra_files=['../audiolizer.yaml', 'assets/midi.js']
        )

