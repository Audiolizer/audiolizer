import math
import numpy as np
import plotly.graph_objs as go
import glob
from collections import defaultdict
import os
from datetime import datetime
import pandas as pd

chromatic_scale = {
    'B#': 0, # B sharp is the same as C
    'C': 0,
    'C#': 1,
    'Db': 1,
    'D': 2,
    'D#': 3,
    'Eb': 3,
    'E': 4, # E is the same as F flat
    'Fb': 4,
    'E#': 5, # F is the same as E sharp
    'F': 5,
    'F#': 6,
    'Gb': 6,
    'G': 7,
    'G#': 8,
    'Ab': 8,
    'A': 9,
    'A#': 10,
    'Bb': 10,
    'B': 11, # B is the same as C flat
    'Cb': 11,}

A4 = 440 # tuning
C0 = A4*pow(2, -4.75)

frequencies = dict(
#     A4 = A4,
#     C0 = C0,
    A0=27.5,
    C2=65.40639,
    C3=130.8128,
    C4=262,
    C5=523.2511,
    C6=1046.502,
    C7=2093.005,
    C8=4186, # high C on piano
)
# -

frequency_marks = {np.log10(v): k for k,v in frequencies.items()}

def midi_note(freq):
    """
    The midi frequency standard is given by
    
    d = 69 + 12*log_2(f/440hz)
    
    https://en.wikipedia.org/wiki/MIDI_tuning_standard"""
    return int(69 + 12*np.log2(freq/440))


def get_scale(notes):
    """converts list of notes to {note value: pitch}
    note values range from [0, 11] in equal temperament
    """
    return {chromatic_scale[_]: _ for _ in notes}


def get_scale_note(note_value, scale):
    """finds the closest note in the scale to a given note value
    note values should be a float the range [0, 11]
    """
    min_diff = 12
    closest_note = 0
    for note, name in scale.items():
        diff = abs(note_value - note)
        if diff < min_diff:
            closest_note = note
            min_diff = diff
    return closest_note


def chromatic_pitch(frequency):
    """determine octave and chromatic note

    note will be a float so we can round to match scale
    """
    h = 12*math.log2(frequency/C0)
    octave = int(h//12)
    n = h % 12 # nth note
    return octave, n



def get_scale_notes(tonic, semitone_sequence):
    """construct note sequence from tonic and semitones

    ex: C major scale
        get_scale_notes('C', '2,2,1,2,2,2,1')

        returns: C, D, E, F, G, A, B

    """
    # Mapping of note to its corresponding semitone number in an octave
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Find starting index from the notes list
    start_index = notes.index(tonic)

    # Split the semitone_sequence input to identify the steps
    steps = semitone_sequence.split(',')

    # Start with the tonic note
    scale = [tonic]

    # Current index in the chromatic scale
    current_index = start_index

    for step in steps:
        # Calculate the number of semitones to move
        semitone_steps = int(step)

        # Update current index and wrap around using modulo 12
        current_index = (current_index + semitone_steps) % 12

        # Append the note at the new index
        scale.append(notes[current_index])

    # Return the scale except the last note to maintain the structure of one octave
    return ','.join(scale[:-1])


def pitch_from_freq(frequency, scale_notes='C,C#,D,D#,E,F,F#,G,G#,A,A#,B'):
    """Convert from frequency to pitch, with optional rounding to C major scale."""
    scale_notes = scale_notes.split(',')
    scale = get_scale(scale_notes)

    octave, note = chromatic_pitch(frequency)

    n = get_scale_note(note, scale)

    pitch_name = scale[n]

    return pitch_name + str(octave)

def freq_from_pitch(note, A4=A4):
    """ convert from pitch to frequency
    
    based on https://gist.github.com/CGrassin/26a1fdf4fc5de788da9b376ff717516e
    """
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    octave = int(note[2]) if len(note) == 3 else int(note[1])
        
    keyNumber = notes.index(note[0:-1]);
    
    if (keyNumber < 3) :
        keyNumber = keyNumber + 12 + ((octave - 1) * 12) + 1; 
    else:
        keyNumber = keyNumber + ((octave - 1) * 12) + 1; 

    return A4 * 2** ((keyNumber- 49) / 12)

def freq_to_degrees(freq):
    """convert input frequency to midi degree standard

    midi degrees are in the range [0, 127]
    """
    return min(127, max(0, int(69+np.floor(12*np.log2(freq/440.)))))

def merge_pitches(beeps):
    merged = []
    last_freq = 0
    last_amp = 0
    for t, freq, amp, dur in beeps:
        # Check if merged is not empty and the current freq matches the last_freq
        if merged and freq == last_freq:
            # if merged[-1][2] < amp_min:  # Checking amplitude of the last entry in 'merged'
            merged[-1][2] = (amp + last_amp) / 2  # Adjusting amplitude
            merged[-1][3] += dur  # Extending duration
            # Note: There's no 'else' block to handle other cases explicitly
        else:
            merged.append([t, freq, amp, dur])
            last_freq = freq
            last_amp = amp
    return merged


def quiet(beeps, min_amp):
    silenced = []
    for t, freq, amp, dur in beeps:
        if amp < min_amp:
            amp = 0
        silenced.append((t, freq, amp, dur))
    return silenced



# unused
# def get_sequence(beeps):
#     """sequence data for midi playback"""
#     t = 0
#     sequence = defaultdict(list)
#     #  freq_, volume_/max_vol, duration
#     for freq_, vol, dur in beeps:
#         sequence['when'].append(t)
#         sequence['pitch'].append(int(math.floor(freq_)))
#         sequence['duration'].append(dur)
#         sequence['volume'].append(.5)
#         t += dur
#     return sequence


def write_plot(fig, fname):
    plot_div = plot(fig, output_type='div', include_plotlyjs='cdn')
    with open(fname, 'w') as f:
        f.write(plot_div)
        f.write('\n')

def write_midi(beeps, tempo, fname, time=0, track=0, channel=0):
    # duration = 60/tempo
    midi_file = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                          # automatically)
    beat_duration = 60./tempo

    midi_file.addTempo(track, time, tempo)

    for freq, amp, dur in beeps: # Hz, [0,1], sec            
        pitch = freq_to_degrees(freq) # MIDI note number
        duration = dur/beat_duration # convert from seconds to beats
        volume = min(127, int(amp*127))  # 0-127, as per the MIDI standard
        midi_file.addNote(track, channel, pitch, time, duration, volume)
        time += duration
    with open(fname, "wb") as output_file:
        midi_file.writeFile(output_file)

def clear_files(fname_glob="assets/*.wav", max_storage=10e6):
    """keep files up to a maximum in storage size (bytes)"""
    files = get_files(fname_glob)
    if files is not None:
        removable = files[files.cumulative > max_storage].fname.values
        for fname in removable:
            if os.path.exists(fname):
                os.remove(fname)
        return removable
    return []


def get_files(fname_glob="assets/*.wav"):
    """retrieve files and metadata"""
    fnames = glob.glob(fname_glob)
    results = defaultdict(list)
    for fname in fnames:
        results['fname'].append(fname)
        results['size'].append(os.path.getsize(fname))
        results['accessed'].append(datetime.fromtimestamp(os.path.getatime(fname)))
    if len(results) > 0:
        files = pd.DataFrame(results).set_index('accessed').sort_index(ascending=False)
        files['cumulative'] = files['size'].cumsum()
        return files


def refactor(df, frequency='1W'):
    """Refactor/rebin the data to a lower cadence

    The data is regrouped using pd.Grouper
    """

    low = df.low.groupby(pd.Grouper(freq=frequency)).min()

    high = df.high.groupby(pd.Grouper(freq=frequency)).max()

    close = df.close.groupby(pd.Grouper(freq=frequency)).last()

    open_ = df.open.groupby(pd.Grouper(freq=frequency)).first()

    average = (open_ + close)/2

    volume = df.volume.groupby(pd.Grouper(freq=frequency)).sum()

    return pd.DataFrame(dict(low=low, high=high, open=open_, close=close, avg=average, volume=volume))

def candlestick_plot(df, base, quote):
    return go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df.open,
                high=df.high,
                low=df.low,
                close=df.close,
                showlegend=False),
            go.Bar(
                x=df.index,
                y=df.volume,
                marker_color='rgba(158,202,225,.5)',
                yaxis='y2',
                showlegend=False),
            ],
        layout=dict(yaxis=dict(title='{} price [{}]'.format(base, quote)),
                    yaxis2=dict(
                        title='{base} volume [{base}]'.format(base=base),
                        overlaying = 'y',
                        side='right'),
                    dragmode='select',
                    margin=dict(l=5, r=5, t=10, b=10),
                    template="plotly_dark",
                   ))



