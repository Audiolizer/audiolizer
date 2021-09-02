# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from html.parser import HTMLParser
import urllib
from collections import defaultdict
import os, json


# %%
class MidiDrumParser(HTMLParser):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self._tab = ''
        self.last_pitch = None
        self.last_instrument = None
        self.last_tag = None
        self.instruments = dict()
        self.paths = dict()
        self.pitches = dict()
        
        result = urllib.request.urlopen(base).read()
        self.feed(result.decode("utf-8"))
    
    def handle_starttag(self, tag, attrs):
        self.last_tag = tag
        pass
    
    def handle_endtag(self, tag):
        pass
    
    def parse_instrument_name(self, line):
        """parse the instrument from the drum line"""
        _, fname, varname = line.split(',')
        fname = fname.split(' ')[-1]
        varname = varname.split(' ')[-1]
        return fname, varname
    
    def handle_data(self, data):
        if (self.last_tag == 'a'):
            if '.' in data:
                if '.js' in data:
                    fname, varname = self.parse_instrument_name(data)
                    self.instruments[self.last_instrument] = varname
                    self.paths[varname] = fname # leave out base
                    self.pitches[varname] = self.last_pitch
                else:
                    pitch, instrument_name = [_.strip() for _ in data.split('.')]
                    self.last_pitch = pitch
                    self.last_instrument = instrument_name


# drums = MidiDrumParser('https://surikov.github.io/webaudiofontdata/sound/drums_6_SBLive_sf2Brush.html')

# %%
class MidiIndexParser(HTMLParser):
    def __init__(self, base="https://surikov.github.io/webaudiofontdata/sound/"):
        super().__init__()
        self.base = base
        self._tab = ''
        self.last_instrument = None
        self.instruments = defaultdict(dict)
        self.paths = defaultdict(dict)
        self.pitches = dict()
        result = urllib.request.urlopen(base).read()
        self.feed(result.decode("utf-8"))
        
    def handle_starttag(self, tag, attrs):
        self._tab = self._tab + '\t'
        if tag == 'a':
            category, instrument = self.last_instrument
            for _ in attrs:
                if 'href' in _:
                    html_path = _[1]
                    if 'drums' in html_path:
                        drums = MidiDrumParser(self.base + html_path)
                        for instrument, preset_varname in drums.instruments.items():
                            if instrument not in self.instruments[category]:
                                self.instruments[category][instrument] = []
                            self.instruments[category][instrument].append(preset_varname)
                            path = drums.paths[preset_varname]
                            self.paths[preset_varname] = self.base + path
                            self.pitches[preset_varname] = drums.pitches[preset_varname]
                    else:
                        preset = html_path.split('.html')[0]
                        preset_varname = '_tone_' + preset
                        self.instruments[category][instrument].append(preset_varname)
                        self.paths[preset_varname] = self.base + preset + '.js'

    def handle_endtag(self, tag):
        self._tab = self._tab[:-2]

    def handle_data(self, data):
        if ':' in data:
            instrument, category = [_.strip() for _ in data.split(':')]
            self.instruments[category][instrument] = []
            self.last_instrument = category, instrument
        elif 'Drums' in data:
            self.last_instrument = 'Drums', ''


# %%
def load_instruments(fname):
    if os.path.exists(fname):
        with open(fname, 'r') as f:
            return json.loads(f.read())
    raise IOError

def get_instruments():
    instruments = load_instruments('instruments.json')
    instrument_paths = load_instruments('instrument_paths.json')
    instrument_pitches = load_instruments('instrument_pitches.json')

    if instruments is None:
        midi_collection = MidiIndexParser()
        instruments = midi_collection.instruments
        instrument_paths = midi_collection.paths
        instrument_pitches = midi_collection.pitches

        with open('instruments.json', 'w') as f:
            f.write(json.dumps(instruments, indent='  '))

        with open('instrument_paths.json', 'w') as f:
            f.write(json.dumps(instrument_paths, indent='  '))

        with open('instrument_pitches.json', 'w') as f:
            f.write(json.dumps(instrument_pitches, indent='  '))
    return instruments, instrument_paths, instrument_pitches

instruments, instrument_paths, instrument_pitches = get_instruments()


# %%
def fetch_instrument_categories(url):
    """category options and initial choice """
    categories = list(instruments)
    return [dict(label=_, value=_) for _ in categories], categories[0]


# %%
def fetch_instrument_types(cat):
    """instrument options and initial choice"""
    instrument_types = list(instruments[cat])
    return [dict(label=_, value=_) for _ in instrument_types], instrument_types[0]


# %%
def relabel_instrument(instrument):
    """parse instrument label
        0240_Chaos_sf2_file
    """
    instrument = instrument.split('sf2')[0]
    return ''.join(instrument.split('_')[3:])


# %%
def fetch_instruments(cat, instrument_type):
    instruments_ = list(instruments[cat][instrument_type])
    first_inst = instruments_[0]
    return [dict(label=relabel_instrument(_), value=_) for _ in instruments_], first_inst


# %%
def fetch_instrument_path(instrument_name):
    return instrument_paths[instrument_name]
