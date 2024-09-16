* debugging date resolution

# 2024-09-16 09:35:16.316738: clock-in: T-40m 

# 2024-09-14 23:13:14.654908: clock-out

* debugging daily candles

# 2024-09-14 22:22:02.276997: clock-in

# 2024-09-14 16:51:28.942469: clock-out

* raising errors in Historic_Crypto

# 2024-09-14 16:45:01.494473: clock-in

# 2024-09-13 16:12:19.859235: clock-out

* debugging cadence
* working frontend with new coinbase api

# 2024-09-13 15:22:09.385451: clock-in

# 2024-09-13 15:01:52.963836: clock-out

* debuging str error

# 2024-09-13 14:18:22.320432: clock-in

# 2024-09-13 12:36:04.403738: clock-out

* fix migrate requirements for Historic Crypto
* Updated Historic_Crypto library, installing from asherp fork
* ValueError: cannot convert float NaN to integer

```sh
Traceback (most recent call last)
File "/home/audiolizer/audiolizer/audiolizer.py", line 592, in play
freq_ = freq_from_pitch(pitch_from_freq(freq_, scale_notes))
File "/home/audiolizer/audiolizer/audiolizer.py", line 190, in pitch_from_freq
octave, note = chromatic_pitch(frequency)
File "/home/audiolizer/audiolizer/audiolizer.py", line 137, in chromatic_pitch
octave = int(h//12)
ValueError: cannot convert float NaN to integer
```

# 2024-09-13 10:29:30.050167: clock-in

# 2024-09-12 13:35:00.472263: clock-out

* Historic Crypto library out of date
https://github.com/Audiolizer/audiolizer/issues/18
https://github.com/David-Woroniuk/Historic_Crypto/issues/17

```py
import http.client
import json
from datetime import datetime

# Convert datetime to Unix timestamp
start = int(datetime.strptime("2024-09-11 00:00:00", '%Y-%m-%d %H:%M:%S').timestamp())
end = int(datetime.strptime("2024-09-13 00:00:00", '%Y-%m-%d %H:%M:%S').timestamp())

# Establish connection
conn = http.client.HTTPSConnection("api.coinbase.com")
payload = ''
headers = {
    'Content-Type': 'application/json'
}

# Make request
conn.request("GET", f"/api/v3/brokerage/market/products/BTC-USD/candles?start={start}&end={end}&granularity=FIFTEEN_MINUTE&limit=28", payload, headers)
res = conn.getresponse()
data = res.read()

# Decode and parse JSON data
decoded_data = data.decode("utf-8")
parsed_data = json.loads(decoded_data)

# Output parsed JSON data
print(parsed_data)
```

# 2024-09-12 13:21:37.113064: clock-in: T-30m 

# 2024-04-19 19:00:55.996430: clock-out

* tonic and mode selection

# 2024-04-19 16:47:46.663170: clock-in

# 2024-04-18 23:21:24.965856: clock-out

* linking to screenshot
* adding screenshot
* control logins with ENABLE_USER_LOGINS

# 2024-04-18 22:56:18.062189: clock-in

# 2024-04-18 17:18:21.519510: clock-out

* fixed google login button
* fixed background colors

# 2024-04-18 15:50:54.263654: clock-in

# 2024-04-17 22:09:39.427236: clock-out: T-10m 

* finishing dark theme

# 2024-04-17 19:45:52.642806: clock-in

# 2024-04-14 15:49:08.766620: clock-out

* styling

# 2024-04-14 15:14:56.456878: clock-in

# 2024-04-08 10:20:50.427506: clock-out

* restyling login, theme

# 2024-04-08 09:29:02.023562: clock-in

# 2024-04-07 19:39:47.630309: clock-out

* login layout dynamically

# 2024-04-07 18:55:20.612962: clock-in

# 2024-04-07 10:10:12.003298: clock-out

* login page

# 2024-04-07 09:11:06.681450: clock-in

# 2024-04-06 21:18:55.351661: clock-out

* working google login

# 2024-04-06 20:03:17.370984: clock-in

# 2024-04-06 17:01:30.182495: clock-out: T-10m 

* test logins

# 2024-04-06 13:12:45.511256: clock-in

# 2024-04-03 20:31:13.106666: clock-out

* adding mongodb, oauth requirements

# 2024-04-03 19:31:28.321408: clock-in

* add dorian scale

# 2024-04-01 17:55:50.474543: clock-out

* added a blues, harmonic, and phrygian scales

# 2024-04-01 16:06:50.944673: clock-in

# 2024-04-01 14:34:01.569842: clock-out

* testing scale mapping

# 2024-04-01 13:14:59.049831: clock-in

# 2024-03-30 21:43:05.902288: clock-out

* c major scale, fix bug in controls for monthly view

# 2024-03-30 19:21:46.589832: clock-in

# 2024-03-30 11:31:04.510556: clock-out

* fixed merge button, simplified interface

# 2024-03-30 09:42:25.594428: clock-in

# 2024-03-29 19:18:12.338480: clock-out

* added avg price, looking at merge logic

# 2024-03-29 17:39:55.071871: clock-in

# 2024-03-17 20:44:18.135016: clock-out

* play on drag select

# 2024-03-17 19:34:48.288799: clock-in

# 2024-03-17 17:07:32.652190: clock-out

* hover and on click play working

# 2024-03-17 13:19:27.841673: clock-in

# 2024-03-16 16:40:59.043638: clock-out: T-30m 

* play on click after pause

# 2024-03-16 15:33:50.378469: clock-in

# 2024-03-16 12:06:58.015767: clock-out

* fixed pause, resume

# 2024-03-16 10:35:16.632156: clock-in

# 2024-03-15 22:25:24.149935: clock-out: T-30m 

* fixing import warnings, logging

# 2024-03-15 20:55:52.058162: clock-in

# 2024-03-15 15:31:59.762361: clock-out

* adding pause button

# 2024-03-15 13:51:37.438675: clock-in

# 2024-03-13 22:20:07.382619: clock-out: T-30m 

* pause and resume

# 2024-03-13 19:26:01.213262: clock-in

# 2024-03-12 17:24:56.817417: clock-out

* adding pause button

# 2024-03-12 17:13:21.857454: clock-in

* set merge defaults to False

# 2024-03-11 00:44:59.425895: clock-out

* got playback to highlight bars

# 2024-03-10 20:12:34.049643: clock-in

# 2024-03-10 18:44:46.180330: clock-out: T-20m 

* adding selectedData feedback

# 2024-03-10 16:39:02.231555: clock-in

# 2024-03-10 15:07:52.003403: clock-out

* stop, play logging time in console
* added play button

# 2024-03-10 14:11:22.854611: clock-in

# 2024-03-10 13:52:09.611833: clock-out: T-10m 

* reviewing webaudiofont

# 2024-03-10 13:29:37.635893: clock-in

# 2024-03-09 12:47:49.710991: clock-out

* fixing build

# 2024-03-09 10:51:49.365956: clock-in

# 2021-10-09 19:23:08.451880: clock-out

* missing half the notes?

# 2021-10-09 19:17:04.033533: clock-in

# 2021-09-03 01:02:33.971182: clock-out: T-1h30m 


# 2021-09-02 22:39:09.461381: clock-in


# 2021-09-02 17:55:58.770527: clock-out: T-1h 

* multi-select among open close high low
* merging
* merge instrument loading

# 2021-09-02 14:07:18.903429: clock-in

# 2021-08-21 21:24:16.509761: clock-out


# 2021-08-21 21:13:23.642095: clock-in

# 2021-08-21 12:38:57.104262: clock-out

* midi sequence prototyping
* fixed dependencies

# 2021-08-21 11:54:36.168205: clock-in

# 2021-09-02 11:39:06.138201: clock-out

* midi playback, fixed bug in today naming convention, volume based duration
* should probably clone and serve webaudiofont locally
* bug: today, tomonth, toweek, toyear should be separate csv (named after granularity)

# 2021-09-02 08:50:28.487655: clock-in

# 2021-08-19 09:30:23.024509: clock-out

* added stop/play sequences

# 2021-08-19 07:11:00.974938: clock-in

# 2021-08-16 14:08:39.194531: clock-out: T-8m 


# 2021-08-16 13:37:51.947884: clock-in

* instrument dropdowns

### 2021-08-15 17:47:41.505140: clock-out: T-17h 


### 2021-08-15 00:16:31.250048: clock-in

### 2021-08-14 02:45:35.237180: clock-out

* added midi dropdowns
feedback from Fox

* remove rests - it hides information
* use constant volume - difficult to perceive volume changes
* major/minor scales for a given sequence

### 2021-08-14 01:54:57.173140: clock-in

### 2021-08-04 22:36:55.872231: clock-out

* got test midi element running
* render sheet music from midi like this https://github.com/cifkao/html-midi-player

### 2021-08-04 22:07:25.286142: clock-in: T-19m 

### 2021-07-31 19:55:31.052014: clock-out

* pushing 0.4.10
* changing default candlesticks

### 2021-07-31 19:14:59.872954: clock-in

### 2021-07-31 16:23:56.168670: clock-out

* got ssl working outside nginx
* moving nginx out
* https://github.com/JonasAlfredsson/docker-nginx-certbot/

### 2021-07-31 13:12:41.014304: clock-in

### 2021-07-29 23:27:40.687115: clock-out: T-1h 

* pine scripting language https://www.tradingview.com/pine-script-reference/

### 2021-07-29 20:29:14.493674: clock-in

### 2021-07-28 20:38:02.961448: clock-out


### 2021-07-28 20:15:12.775935: clock-in

### 2021-07-28 10:43:25.494735: clock-out

* pushing to 0.4.9
* fixing end date

### 2021-07-28 10:33:07.254105: clock-in

### 2021-07-27 23:19:02.300510: clock-out

* pushing 0.4.8
* fixed data gap from writting end date

### 2021-07-27 22:27:42.834487: clock-in

### 2021-07-27 20:49:35.835828: clock-out

* start9 on ch
* getting `0.0.0.0:80 failed (13: Permission denied)` from nginx
* https://github.com/tiangolo/meinheld-gunicorn-flask-docker how to ssl?
* fastapi-dash https://github.com/rusnyder/fastapi-plotly-dash
* nice compose file for nginx 

https://github.com/docker/awesome-compose/tree/master/nginx-wsgi-flask

### 2021-07-27 18:53:57.558991: clock-in

### 2021-07-27 16:48:00.801242: clock-out

* fixing time range bug

### 2021-07-27 16:36:40.139713: clock-in

### 2021-07-26 22:58:40.990389: clock-out

* pushing apembroke/audiolizer:0.4.6

### 2021-07-26 21:14:01.124340: clock-in

### 2021-07-26 01:24:33.329599: clock-out

* adding profiler info
* fixed data gap caused by end date writing

### 2021-07-25 23:48:43.945245: clock-in

### 2021-07-25 00:00:18.150461: clock-out: T-1h 

* resolving data gaps

### 2021-07-24 21:10:36.285458: clock-in

### 2021-07-24 18:53:07.180390: clock-out

* adding cadence files

### 2021-07-24 17:08:14.594734: clock-in

### 2021-07-24 14:26:39.619830: clock-out

* experimenting with cbpro, parameterizing granularity for historical query
* looking at cbpro api


> **Caution**: Historical rates should not be polled frequently.
> If you need real-time information, use the trade and book
> endpoints along with the websocket feed.
> 
> The maximum number of data points for a single request is 200
> candles. If your selection of start/end time and granularity
> will result in more than 200 data points, your request will be
> rejected. If you wish to retrieve fine granularity data over a
> larger time range, you will need to make multiple requests with
> new start/end ranges.


### 2021-07-24 12:49:30.340861: clock-in

### 2021-07-22 23:40:16-04:00: clock-out

* had to fix bug in hourly to support clocking in with time adjustment combined with message
* Audio based qr codes for machine-to-machine communication. non-human frequencies?
* 3d printing for brail

### 2021-07-22 22:18:35.634973: clock-in: T-1h meeting with Gary, audio-markets.com working


### 2021-07-21 22:16:04.844979: clock-out

* fixed date range to match candlestick, viewing exactly 24 hrs

### 2021-07-21 21:12:39.575147: clock-in

### 2021-07-20 23:49:23.584658: clock-out

* fixed data gap
* yesterday's date gets overwritten when switching from `1d` -> `1w`

### 2021-07-20 22:11:47.205082: clock-in

### 2021-07-19 22:33:01.462182: clock-out

* reverting timezone selection, too buggy

### 2021-07-19 21:19:53.074825: clock-in

### 2021-07-17 00:08:26.783140: clock-out: T-90m 


### 2021-07-16 21:55:02.014683: clock-in

### 2021-07-16 18:42:02.356385: clock-out

* nans are getting into time history

### 2021-07-16 17:48:06.108243: clock-in

### 2021-07-16 00:45:19.851415: clock-out

* fixed timezone bugs
* making the candlestick div an output of a callback

### 2021-07-15 22:00:42.033750: clock-in

### 2021-07-13 21:58:44.866482: clock-out

* timezone not updating

### 2021-07-13 19:02:36.267901: clock-in

### 2021-07-13 18:35:44.693731: clock-out

* using scripts only

### 2021-07-13 18:23:27.424677: clock-in

### 2021-07-12 17:26:13.055340: clock-out

* add random walk . start at 100, add or subtract %5

### 2021-07-12 17:20:57.875340: clock-in

### 2021-07-12 13:15:13.360816: clock-out


### 2021-07-12 13:12:50.258447: clock-in

### 2021-07-11 22:18:53.811305: clock-out

* looking for better source of price data

### 2021-07-11 22:09:08.999063: clock-in

### 2021-07-11 20:01:48.592014: clock-out

* pushed 0.4.4
* fetching to current time
* separating today from history

### 2021-07-11 17:13:25.693903: clock-in

### 2021-07-11 00:19:27.392712: clock-out: T-30m 

* Relaxshi latin percrussion instruments
* dxy indicator - the dollar?

### 2021-07-10 22:39:03.298483: clock-in

### 2021-07-10 16:53:52.536370: clock-out

* removing gap logic for now
* manual sync
* refactoring history

### 2021-07-10 15:05:23.859541: clock-in

### 2021-07-09 20:23:02.366858: clock-out

* fixed date fetching

### 2021-07-09 19:31:56.325477: clock-in

### 2021-07-09 02:12:29.621803: clock-out: T-1h 

* fetching in batch

### 2021-07-08 23:10:17.085199: clock-in

### 2021-07-08 01:54:10.939607: clock-out

* querying in batches
* added link to ariagora

### 2021-07-07 23:29:29.646292: clock-in

### 2021-07-06 23:42:37.763553: clock-out: T-15m 

* creating ssl cert

### 2021-07-06 23:05:10.961610: clock-in

### 2021-07-06 20:42:59.070321: clock-out

* running docker-compose in background. not sure why april keeps loading

### 2021-07-06 20:28:36.899523: clock-in: T-20m 

### 2021-07-06 11:58:10.830539: clock-out

* removing cache sizes from production

### 2021-07-06 11:38:02.823668: clock-in: T-10m 

### 2021-07-06 01:58:45.464038: clock-out

* worked with Randy to set up audiolizer.ariagora.com
* hyperlinking localhost
* clarification of mounting options
* mounting pwd into container instead of temporary directories
* adding .env instructions
* updating docker-compose instructions

### 2021-07-05 23:03:23.315253: clock-in

### 2021-07-05 14:21:49.553095: clock-out

* fixed logo favicon

### 2021-07-05 12:33:12.753795: clock-in

* removing src mount from production

### 2021-07-03 14:35:53.010888: clock-out

* adding gunicorn
* `gunicorn==20.1.0`

### 2021-07-03 12:14:24.538693: clock-in

### 2021-07-03 00:53:49.489949: clock-out

* looking at umbrel submission procedure
* How to build cross-platform
```console
docker buildx build --platform linux/arm64,linux/amd64 --tag apembroke/audiolizer:0.4.1 --output "type=registry" .
```
* added LICENSE file

### 2021-07-02 23:58:07.637725: clock-in

### 2021-07-02 02:38:04.026531: clock-out: T-30m 

* activating jupytext
* adding jupytext
* running docker in docker: `docker run -it -v /var/run/docker.sock:/var/run/docker.sock docker`

### 2021-07-02 01:20:37.871837: clock-in

### 2021-07-01 21:54:04.012894: clock-out: T-10m 

* fixed up environment variables

### 2021-07-01 21:02:06.092723: clock-in

### 2021-07-01 00:21:48.695052: clock-out

* slimed down image

### 2021-06-30 23:27:37.784010: clock-in

### 2021-06-30 21:58:17.069562: clock-out: T-30m 


### 2021-06-30 21:17:29.237422: clock-in

### 2021-06-30 00:25:43.952103: clock-out

* slimming down pip packages
Trying to conda install the following

```Dockerfile
RUN source /venv/bin/activate \
 && pip install  \
	audiogen-p3 MIDIUtil \
	dash-bootstrap-components \
 && pip install git+https://github.com/predsci/psidash.git
```
* dash-daq has a conda-forge recipe
* building Historic-Crypto from conda skeleton


### 2021-06-29 23:17:03.409827: clock-in

### 2021-06-29 21:49:15.649821: clock-out

* multi stage fixes
* adding bash init
* keeping environment active
* correcting conda init
* switching to named environment audiolizer
* correcting environment name
* formatting
* multi-stage build


* using conda-pack to slim down images https://pythonspeed.com/articles/conda-docker-image-size/

### 2021-06-29 17:57:57.782630: clock-in

### 2021-06-27 14:24:34.558294: clock-out

* dash react tutorial

### 2021-06-27 11:33:47.637563: clock-in

### 2021-06-27 10:19:16.480666: clock-out: T-15m 

* reading up on react-dash https://dash.plotly.com/react-for-python-developers

### 2021-06-27 09:30:13.979558: clock-in

### 2021-06-26 22:18:21.224806: clock-out

* pushed apembroke/audiolizer:0.4
* added ticker options

### 2021-06-26 19:09:39.374354: clock-in

### 2021-06-26 18:09:56.490850: clock-out

* responsive resizing
* `app.clientside_callback`?

### 2021-06-26 16:29:02.448030: clock-in

* alternative price data: bitstamp, crypto.com

### 2021-06-26 01:25:53.646217: clock-out

* fixed data gap

### 2021-06-26 00:32:14.224878: clock-in

### 2021-06-25 23:28:40.701319: clock-out

* found price nans
* shrinking RUN command
* compressing docker image

### 2021-06-25 21:55:24.815029: clock-in

### 2021-06-24 23:18:45.354779: clock-out

* switching to bootstrap
* adding to current time to include more data

### 2021-06-24 21:51:49.598071: clock-in

### 2021-06-24 19:36:26.101766: clock-out

* added csv compression, price files cache limit, initial start date
* adding hourly promo
* added python install instructions, fixed graph
* adding open-dyslexic font
* disabled draggable select
* higher cadence options

### 2021-06-24 17:37:26.100709: clock-in

### 2021-06-24 13:30:10.823467: clock-out

* meeting with Randy
* include version number in interface
* arpeggio?

### 2021-06-24 13:06:50.585857: clock-in

### 2021-06-23 23:26:02.451923: clock-out

* got date radio buttons working
* adding date range radio options
* adding jupytext

### 2021-06-23 22:10:34.591225: clock-in

### 2021-06-23 02:30:03.974096: clock-out: T-30m 

* mounting source into container
* added toggle for price type

### 2021-06-23 00:56:00.880577: clock-in

### 2021-06-22 23:57:20.974732: clock-out: T-5m 

* adding docker-compose

### 2021-06-22 23:42:55.152875: clock-in

### 2021-06-22 00:09:27.107340: clock-out

* pushing apembroke/audiolizer:0.2
* fixed bug in import
* sample midi

### 2021-06-21 23:57:58.681256: clock-in

* adding sample midi

### 2021-06-21 23:36:47.974003: clock-out

* added favicon
* moving into assets
* icon courtesy of SiLVa
* adding screen shot
* ignoring wav and midi
* added cache setting
* filling data gaps
* irig 2 setup

### 2021-06-21 20:06:43.967497: clock-in

### 2021-06-21 18:52:53.877091: clock-out

* fixing data gaps

### 2021-06-21 17:59:56.336985: clock-in

### 2021-06-20 16:03:45.241495: clock-out

* meeting with Randy

1. add floor function to normalize frequencies - accomplished through pitch conversion
1. slider that controls modulus on frequency [1, 100] so melody can cycle
1. 3 market displays - monthly, weekly, daily - put into a dial - multiple rows
1. umbrel as a distribution mechanism - be a good citizen w.r.t. disk space
1. estimate footprint of settings (size of files generated)
1. icon and screen shots
1. umbrel uses tor - is that a problem for coinbase price api? Consider privacy - Can this expose user's ip address?
1. scales - ease of use toggle between cmajor and aminor work well together
1. how to achieve harmony and melody is in the relationship between major and minor scales
1. market data would be like trebble clef (middle c and above) and another market feed as the bass clef (middle c and below) - lower case c is middle c - automated sheet music will help alot
1. weekly candles could be base cleff. hourly could be trebble
1. allow open/high/low/close selection - this is the same in music
1. audiolizer sounds great on the phone!
1. btc ledger as data source? umbrel platform gives access to all kinds of btc data...

required reading
On the Sensations of Tone - Helmholtz
The Study of Counterpoint: From Johann Joseph Fux's Gradus Ad Parnassum

### 2021-06-20 14:39:47.114093: clock-in

### 2021-06-20 00:38:28.710038: clock-out

* pushing docker version
* looking at html midi players:
* https://github.com/cifkao/html-midi-player javascript - but how to embed?
* https://surikov.github.io/webaudiofont/ this is a really beautiful html-only midi system. we could build a dash component around this. That would open the door to custom instruments, etc.

* added midi download

### 2021-06-19 21:56:47.016441: clock-in

### 2021-06-19 20:14:25.744423: clock-out

* changed src to github raw

### 2021-06-19 20:13:50.087569: clock-in: T-4m 

### 2021-06-19 20:08:24.558530: clock-out

* a better sample illustrating duration

### 2021-06-19 19:37:22.200467: clock-in

### 2021-06-19 00:43:59.135736: clock-out

* added code highlighting
* sample audio
* fixed site name

### 2021-06-19 00:43:16.152887: clock-in: T-14m 

### 2021-06-19 00:28:38.532399: clock-out

* added worklog

### 2021-06-19 00:05:44.387679: clock-in

### 2021-06-19 00:02:40.078861: clock-out

* documentation improvements

### 2021-06-18 22:10:09.398018: clock-in

### 2021-06-18 21:07:39.810058: clock-out

* adding docs
* removed legend, added docs

### 2021-06-18 18:47:04.388103: clock-in

* you can calculate the % data loaded by comparing list of missing files to those present

### 2021-06-18 00:25:05.504006: clock-out

* updating instructions
* running from audiolizer subdir

Running without temp directories:
```console
docker run -p 8051:8051 -it apembroke/audiolizer

```

Running from temp directories:

```console
docker run -v /tmp/audio_files:/home/audiolizer/audiolizer/assets -v /tmp/price_data:/home/audiolizer/audiolizer/history -p 8051:8051 -it apembroke/audiolizer
```
* setting environment variable
* moving install paths
* creating cache directories
* building docker image
* building docker image from clean git repo

```console
git archive --format=tar --prefix=audiolizer/ HEAD | (cd /tmp && tar xf -)
docker build -t apembroke/audiolizer -f /tmp/audiolizer/Dockerfile /tmp/audiolizer
```
* adding midi
* tempo in yaml
* added tempo
* midi example

```python
from midiutil import MIDIFile

degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 60   # In BPM
volume   = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(degrees):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

with open("major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
```

### 2021-06-17 22:29:08.889910: clock-in

### 2021-06-17 21:59:46.147344: clock-out

* allowing date range to load on the fly
Check out ableton, midi

8 measures, 4/4 time, 
push the tempo.. 1440 beats per minute
3 hour candles? 8 beats

### 2021-06-17 21:34:12.651429: clock-in

### 2021-06-15 23:29:37.846516: clock-out

* saving historical data in daily files

### 2021-06-15 21:52:35.466441: clock-in

### 2021-06-14 23:36:15.632618: clock-out: T-45m 


### 2021-06-14 22:03:32.676556: clock-in

### 2021-06-13 23:38:42.855196: clock-out: T-10m 

* added sub range select

### 2021-06-13 22:32:12.627082: clock-in

### 2021-06-13 16:40:53.909382: clock-out

* testing start,end playback

### 2021-06-13 15:57:20.258581: clock-in

### 2021-06-13 13:11:47.189135: clock-out: T-10m 

* building in docker

### 2021-06-13 11:44:34.643876: clock-in

### 2021-06-12 23:44:04.566372: clock-out: T-10m 


### 2021-06-12 23:32:14.026151: clock-in

### 2021-06-12 23:15:40.277053: clock-out

* added rests toggle

### 2021-06-12 23:04:15.082670: clock-in

### 2021-06-12 14:00:50.574441: clock-out

* merge toggle

### 2021-06-12 12:50:03.490012: clock-in

### 2021-06-10 22:50:35.107916: clock-out

* merging by amplitude

### 2021-06-10 21:26:00.698998: clock-in

### 2021-06-10 21:25:20.990707: clock-out


### 2021-06-10 20:33:18.558354: clock-in

### 2021-06-10 01:05:01.630823: clock-out

* merged pitches, added rests, tone pitch dropdown

### 2021-06-09 22:56:32.687035: clock-in

### 2021-06-08 22:24:48.237340: clock-out

* added pitch range slider

### 2021-06-08 20:36:05.302294: clock-in

### 2021-05-31 12:01:32.717887: clock-out


### 2021-05-31 11:48:25.059119: clock-in

### 2021-05-31 11:24:43.444204: clock-out: T-13h 


### 2021-05-30 19:57:04.403863: clock-in

### 2021-05-30 19:30:13.440804: clock-out: T-1h 


### 2021-05-30 17:28:19.136269: clock-in

### 2021-05-30 02:33:40.434820: clock-out

* basic dash layout, test beeping, loading price history

### 2021-05-30 02:32:35.340810: clock-in: T-1h 

### 2021-05-29 23:18:41.414068: clock-out: T-1h 


### 2021-05-29 20:06:06.278965: clock-in

### 2021-05-29 19:54:28.225556: clock-out: T-3h 

* installing requirements


### 2021-05-29 15:49:10.496087: clock-in

