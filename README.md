
## [AUDIOLIZER](https://github.com/Audiolizer/audiolizer)
#### Market audiolization dashboard



![Market audiolizer screenshot](https://github.com/asherp/audiolizer/raw/master/audiolizer0.2_screen_shot.png)

Here is the [midi file](https://github.com/asherp/audiolizer/raw/master/docs/assets/BTC_2020-09-01_2021-06-21_1W_C3_C5_pitch_25_75_240bpm_merged_rests.midi) for the above plot.

Visit the documenation site to learn [how it works](https://asherp.github.io/audiolizer/About/)!

## Requirements

* numpy
* pandas
* plotly
* Historic-Crypto (pip)
* PyAudio==0.2.11 (conda)
* audiogen_p3 pip install audiogen_p3
* MIDIUtil==1.2.1 (pip)
* psidash `pip install git+https://github.com/predsci/psidash.git`
* dash bootstrap components `pip install dash-bootstrap-components`
* dash audio components (wav) `pip install dash-audio-components`
* dash daq `pip install dash-daq`

docs dependences (optional)

* mkdocs (pip)
* tabulate (pip)

# Running from python

```shell
git clone https://github.com/asherp/audiolizer \
cd audiolizer \
python audiolizer.py
```

You should see something like the following output

```
audiolizer temp data: ./history/
Dash is running on http://0.0.0.0:8051/
* Serving Flask app 'audiolizer' (lazy loading)
* Environment: production
	- WARNING: This is a development server. Do not use it in a production deployment.
	- Use a production WSGI server instead.
* Debug mode: on

```
Open your browser to [http://localhost:8051](http://localhost:8051)

You may hear a startup sound when the application starts. If you don't, that's ok - the dashboard will still play through the browser! 

# Running from Docker

## option 1: docker-compose

Now run the audiolizer application:

```console
docker-compose up audiolizer
```
This will automatically mount the audiolizer repo into the container's `/home/audiolizer` directory.

Open your browser to [http://localhost:80](http://localhost:80)

## option 2: docker run

Running without mounting the repo into container:

```console
docker run -p 8051:8051 -it apembroke/audiolizer
```

## option 3: docker run with temp directories mounted

Running with mounted temp directories:

```shell
docker run -v /tmp/audio_files:/home/audiolizer/audiolizer/assets -v /tmp/price_data:/home/audiolizer/audiolizer/history -p 8051:8051 -it apembroke/audiolizer
```

