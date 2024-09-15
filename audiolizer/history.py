# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# Objective: get_history should fetch all the data at once then save it to separate files.

import logging
logger = logging.getLogger(__name__)
fhandler = logging.FileHandler(filename='audiolizer.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)

# + active="ipynb"
# import logging
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# logging.debug("test")

# +
import pytz
import sys
sys.path.append('.')
from Historic_Crypto import HistoricalData
import pandas as pd
import os
from datetime import datetime

def get_timezones(url):
    return [dict(label=v, value=v) for v in pytz.all_timezones]

#these are the granularities available from the new coinbase api
# Should these replace valid_granularities?
API_GRANULARITIES = {
   60: 'ONE_MINUTE',
    300: 'FIVE_MINUTE',
    900: 'FIFTEEN_MINUTE',
    1800: 'THIRTY_MINUTE',
    3600: 'ONE_HOUR',
    7200 : 'TWO_HOUR',
    21600: 'SIX_HOUR',
    86400: 'ONE_DAY'
}


valid_granularities = [60, 300, 900, 3600, 21600, 86400]
granularity = int(os.environ.get('AUDIOLIZER_GRANULARITY', 300)) # seconds

# see api for valid intervals https://docs.pro.coinbase.com/#get-historic-rates
assert granularity in valid_granularities

audiolizer_temp_dir = os.environ.get('AUDIOLIZER_TEMP', './history')
logger.info('audiolizer temp data: {}'.format(audiolizer_temp_dir))

max_age = pd.Timedelta(os.environ.get('AUDIOLIZER_MAX_AGE', '5m'))
logger.info('audiolizer max daily age {}'.format(max_age))

def get_granularity(cadence):
    """Get query granularity for the current cadence
        
    We need the query granularity to be within the valid granularities
    The cadence needs to be a multiple of the granularity
    """
    dt = pd.Timedelta(cadence).total_seconds()
    for _ in valid_granularities[::-1]:
        if (_ <= dt) & (dt%_ == 0):
            return _
    raise NotImplementedError('cannot find granularity for cadence {}'.format(cadence))

def file_cadence(granularity):
    """Set the resolution of the file"""
    if granularity < 60*60*24:
        return '1D'
    else:
        return '1M'    

def refactor(df, frequency='1W'):
    """Refactor/rebin the data to a lower cadence

    The data is regrouped using pd.Grouper
    """
    low = df.low.groupby(pd.Grouper(freq=frequency)).min()
    high = df.high.groupby(pd.Grouper(freq=frequency)).max()
    close = df.close.groupby(pd.Grouper(freq=frequency)).last()
    open_ = df.open.groupby(pd.Grouper(freq=frequency)).first()
    volume = df.volume.groupby(pd.Grouper(freq=frequency)).sum()
    return pd.DataFrame(dict(low=low, high=high, open=open_, close=close, volume=volume))


def load_date(ticker, granularity, int_):
    logger.info('loading single date {}'.format(int_))
    start_ = int_.left.strftime('%Y-%m-%d-%H-%M')
    end_ = int_.right.strftime('%Y-%m-%d-%H-%M')
    try:
        return HistoricalData(ticker,
                              granularity,
                              start_,
                              end_,
                              ).retrieve_data()
    except:
        logger.warning('could not load using {} {}'.format(start_, end_))
        raise


def get_gaps(df, granularity):
    new_ = refactor(df, '{}s'.format(granularity))
    return new_[new_.close.isna()]


def fetch_data(ticker, granularity, start_, end_):
    """Need dates in this format %Y-%m-%d-%H-%M"""
    try:
        return HistoricalData(ticker,
                              granularity,
                              start_,
                              end_,
                              ).retrieve_data()
    except:
        logger.warning('could not load using {} {}'.format(start_, end_))
        raise


def write_data(df, ticker, granularity):
    """write data grouped by date
    
    Note: data gaps will result if a partial day provided.
    Make sure data is complete before passing to this function
    """
    # this breaks when df is a single date
    for t, group in df.groupby(pd.Grouper(freq='1D')):
        tstr = t.strftime('%Y-%m-%d-%H-%M')
        fname = audiolizer_temp_dir + '/{}-{}-{}.csv.gz'.format(
                ticker, granularity, t.strftime('%Y-%m-%d'))
        group.to_csv(fname, compression='gzip')
        logger.info('wrote {}'.format(fname))
        
def fetch_missing(files_status, ticker, granularity):
    """Iterate over batches of missing dates"""
    for batch, g in files_status[files_status.found==0].groupby('batch', sort=False):
        t1, t2 = g.iloc[[0, -1]].index
        # extend by 1 day whether or not t1 == t2
        t2 += pd.Timedelta('1D')
        endpoints = [t.strftime('%Y-%m-%d-%H-%M') for t in [t1, t2]]
        logger.info('fetching {}, {}'.format(len(g), endpoints))
        df = fetch_data(ticker, granularity, *endpoints).loc[t1:t2] # only grab data between endpoints
        write_data(df[df.index < t2], ticker, granularity)

        
def get_files_status(ticker, granularity, start_date, end_date):
    start_date = pd.to_datetime(start_date.date())
    end_date = pd.to_datetime(end_date.date())
    fnames = []
    foundlings = []
    dates = []
    batch = []
    batch_number = 0
    last_found = -1
    for int_ in pd.interval_range(start_date, end_date):
        dates.append(int_.left)
        fname = audiolizer_temp_dir + '/{}-{}-{}.csv.gz'.format(
            ticker, granularity, int_.left.strftime('%Y-%m-%d'))
        found = int(os.path.exists(fname))
        foundlings.append(found)
        if found != last_found:
            batch_number += 1
        last_found = found
        batch.append(batch_number)
        fnames.append(fname)
    files_status = pd.DataFrame(dict(files=fnames, found=foundlings, batch=batch), index=dates)
    return files_status


# + active="ipynb"
# files_status = get_files_status('BTC-USD',
#                                 300, # 2021-07-27 00:00:00 -> 2021-07-29 00:00:00
#                                 pd.to_datetime('2021-07-27 00:00:00'),
#                                 pd.to_datetime('2021-07-29 00:00:00'))
#
# files_status
# -

def get_today_GMT():
    # convert from system time to GMT
    system_time = pd.Timestamp(datetime.now().astimezone())
    today = system_time.tz_convert('GMT').tz_localize(None)
    return today


# * getting BTC-USD files status: 2021-07-20 00:00:00 -> 2021-07-21 03:50:49.619707
# * INFO:history:getting BTC-USD files status: 2021-07-20 00:00:00 -> 2021-07-21 04:07:48.872110
# * 2021-07-14 00:00:00 -> 2021-07-21 04:07:22.738431

# +
def get_today(ticker, granularity):
    today = get_today_GMT()
    tomorrow = today + pd.Timedelta('1D')
    start_ = '{}-00-00'.format(today.strftime('%Y-%m-%d'))
    end_ = today.strftime('%Y-%m-%d-%H-%M')
    try:
        df = HistoricalData(ticker,
                            granularity,
                            start_,
                            end_,
                            ).retrieve_data()
        return df
    except:
        logger.warning('could not load using {} {}'.format(start_, end_))
        raise


def get_age(fname):
    """Get the age of a given a file"""
    st=os.stat(fname)    
    mtime=st.st_mtime
    return pd.Timestamp.now() - datetime.fromtimestamp(mtime)

        
def get_history(ticker, granularity, start_date, end_date = None):
    """Fetch/load historical data from Coinbase API at specified granularity
    
    Data loaded from start_date through end of end_date
    params:
        start_date: (str) (see pandas.to_datetime for acceptable formats)
        end_date: (str)
        granularity: (int) seconds (default: 300)

    price data is saved by ticker and date and stored in audiolizer_temp_dir
    
    There are two timezones to keep track of. Assume input in GMT
    system timezone: the timezone of the machine the audiolizer is run from
    GMT: the timezone that price history is fetched/stored in
    """
    start_date = pd.to_datetime(start_date)

    today = get_today_GMT() #tz-naive but value matches GMT

    if end_date is None:
        # don't include today
        end_date = today + pd.Timedelta('1d')
        logger.info('no end_date provided, using {}'.format(end_date))
    else:
        # convert the user-specified date and timezone to GMT
        end_date = pd.to_datetime(end_date)
        # prevent queries from the future
        end_date = min(today, end_date) + pd.Timedelta('1d')
        logger.info('using end_date {}'.format(end_date))
    
    assert start_date <= end_date
    
    logger.info('getting {} {}s files status: {} -> {}'.format(ticker, granularity, start_date, end_date))
    files_status = get_files_status(ticker, granularity, start_date, end_date)
    files_status = files_status[files_status.index < pd.to_datetime(today.date())]
    fetch_missing(files_status, ticker, granularity)
    
    if len(files_status) == 0:
        raise IOError('Could not get file status for {}'.format(ticker, start_date, end_date))

    df = pd.concat(map(lambda file: pd.read_csv(file, index_col='time', parse_dates=True, compression='gzip'),
                         files_status.files)).drop_duplicates()

    if end_date >= today:
        logger.info('end date is today!')
        # check age of today's data. If it's old, fetch the new one
        today_fname = audiolizer_temp_dir + '/{}-{}-today.csv.gz'.format(ticker, granularity)
        if os.path.exists(today_fname):
            if get_age(today_fname) > max_age:
                logger.info('{} is too old, fetching new data'.format(today_fname))
                today_data = get_today(ticker, granularity)
                today_data.to_csv(today_fname, compression='gzip')
            else:
                logger.info('{} is not that old, loading from disk'.format(today_fname))
                today_data = pd.read_csv(today_fname, index_col='time', parse_dates=True, compression='gzip')
        else:
            logger.info('{} not present. loading'.format(today_fname))
            today_data = get_today(ticker, granularity)
            today_data.to_csv(today_fname, compression='gzip')
        df = pd.concat([df, today_data]).drop_duplicates()
    return df.astype(float)

# + active="ipynb"
# to = get_today('BTC-USD', 300)

# + active="ipynb"
# hist = get_history('BTC-USD', 300, '2021-07-20', '2021-07-26')

# + active="ipynb"
# from audiolizer import candlestick_plot
# from plotly import graph_objs as go
#
# from plotly.offline import init_notebook_mode
# init_notebook_mode(connected=True)
#
# # candlestick_plot(refactor(hist, '7D'), 'BTC', 'USD')
#
# candlestick_plot(hist, 'BTC', 'USD')
# -

# Show today's prices

# + active="ipynb"
# today_file = 'history/BTC-USD-today.csv.gz'
# pd.read_csv(today_file, index_col='time', parse_dates=True, compression='gzip')
# -

# ## Testing historic data
#
# > The maximum number of data points for a single request is 200
# > candles. If your selection of start/end time and granularity
# > will result in more than 200 data points, your request will be
# > rejected. If you wish to retrieve fine granularity data over a
# > larger time range, you will need to make multiple requests with
# > new start/end ranges.

# + active="ipynb"
# start = pd.to_datetime('July 20, 2011')
# end = pd.to_datetime('July 24, 2021')
# cadence = 86400 # 1d
# len(pd.date_range(start, end, freq='{}s'.format(cadence)))
# -

# Historical data apparently batches automatically, while cbpro does not.
#
# We could poll at a lower cadence and keep seperate file cadences based on that.

# + active="ipynb"
# hist = HistoricalData('BTC-USD',
#               cadence,
#               start.strftime('%Y-%m-%d-%H-%M'),
#               end.strftime('%Y-%m-%d-%H-%M'),
#               ).retrieve_data()
