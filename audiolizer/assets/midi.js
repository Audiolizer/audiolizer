// -*- coding: utf-8 -*-
var AudioContextFunc = window.AudioContext || window.webkitAudioContext;
var audioContext = new AudioContextFunc();
var player=new WebAudioFontPlayer();
var instr=null;
var base = 'https://surikov.github.io/webaudiofontdata/sound/';

player.loader.decodeAfterLoading(audioContext, '_tone_0250_SoundBlasterOld_sf2');

var sound_library = {
  "_tone_0250_SoundBlasterOld_sf2": _tone_0250_SoundBlasterOld_sf2,
  }

// audioContext - AudioContext
// target - a node to connect to, for example audioContext.destination
// preset - variable with the instrument preset
// when - when to play, audioContext.currentTime or 0 to play now, audioContext.currentTime + 3 to play after 3 seconds
// pitch - note pitch from 0 to 127, for example 2+12*4 to play D of fourth octave (use MIDI key for drums)
// duration - note duration in seconds, for example 4 to play 4 seconds
// volume - 0.0 <=1.0 volume (0 is ‘no value’, ‘no value’ is 1)
// slides - array of pitch bends

// queueWaveTable(audioContext, target, preset, when, pitch, duration, volume, slides)


function updateTimestampStore(timestamp) {
    const inputElement = document.getElementById('timestamp-input');
    inputElement.value = timestamp; // Update the value

    // Manually trigger a "change" event for the input element
    var event = new Event('change', { 'bubbles': true });
    inputElement.dispatchEvent(event);
}


var isPlaying = false; // Tracks if the sequence is currently playing
var audioContextTimeAtStart = 0; // When the playback was started
var lastPauseTime = 0; // When the playback was paused


function play_sequence(preset, notes, startFrom = 0) {
    window['envelope'] = [];
    window['timeoutIDs'] = [];
    audioContextTimeAtStart = audioContext.currentTime;

    const scheduleNote = (t, when, pitch, duration, volume) => {
        var timeoutID = setTimeout(() => {
            // console.log(`Playing note at timestamp: ${t}`);
            
            // Call updateTimestampStore here to update the hidden input's value
            updateTimestampStore(t);

        }, when * 1000); // Convert 'when' to milliseconds
        window['timeoutIDs'].push(timeoutID);
    };

    for (var n = 0; n < notes['when'].length; n++) {
        t = notes['t'][n]
        when = notes['when'][n];
        pitch = notes['pitch'][n];
        duration = notes['duration'][n];
        volume = notes['volume'][n];

        if (when >= startFrom) {
            // Schedule each note by calling the function that creates a closure
            scheduleNote(t, when, pitch, duration, volume);

            var envelope = player.queueWaveTable(
                audioContext,
                audioContext.destination,
                window[preset],
                audioContext.currentTime + when,
                Math.max(parseInt(pitch), 0),
                Math.max(duration, 0),
                Math.max(volume, 0)
                );
            window['envelope'].push(envelope);
        }
    }
}

function stop_sequence(){
    // Cancel all scheduled envelopes for sound playback
    if (typeof window['envelope'] !== 'undefined') {
        console.log('stopping envelopes');
        window['envelope'].forEach(function(envelope) {
            envelope.cancel(); 
        });
        window['envelope'] = []; // Clear the envelopes array after stopping
    } else {
        console.log('no envelopes to cancel');
    }

    // Clear all scheduled setTimeout calls to prevent logging
    if (typeof window['timeoutIDs'] !== 'undefined' && window['timeoutIDs'].length > 0) {
        console.log('stopping scheduled logs');
        window['timeoutIDs'].forEach(function(timeoutID) {
            clearTimeout(timeoutID);
        });
        window['timeoutIDs'] = []; // Clear the timeoutIDs array after clearing timeouts
    } else {
        console.log('no scheduled logs to cancel');
    }
}

function loadAndPlaySequence(preset, path, notes, startFrom) {
    if (typeof window[preset] !== 'undefined') {
        console.log('Variable ' + preset + ' exists!');
        play_sequence(preset, notes, startFrom);
    } else {
        console.log('Loading ' + preset + ' from ' + path);
        player.loader.startLoad(audioContext, path, preset);
        player.loader.waitLoad(function() {
            instr = window[preset];
            play_sequence(preset, notes, startFrom);
        });
    }
}


window.dash_clientside = Object.assign({}, window.dash_clientside, {
    dash_midi: {
        play: function(n_clicks, preset, path, notes) {
            if (n_clicks % 2 === 0) { // Even n_clicks: attempt to pause
                if (isPlaying) {
                    stop_sequence();
                    lastPauseTime = audioContext.currentTime - audioContextTimeAtStart;
                    isPlaying = false;
                    console.log('Paused at: ', lastPauseTime, 'seconds');
                }
            } else { // Odd n_clicks: play or resume
                if (!isPlaying) {
                    if (lastPauseTime > 0) {
                        // Resuming
                        stop_sequence();
                        console.log('Resuming at ', startFrom);
                        startFrom = lastPauseTime;
                        loadAndPlaySequence(preset, path, notes, startFrom);
                    } else {
                        // Starting fresh
                        console.log('Playing');
                        stop_sequence(); // Ensure any previous sequence is stopped
                        startFrom = 0;
                        loadAndPlaySequence(preset, path, notes, startFrom);
                    }
                    isPlaying = true;
                }
            } // This closing brace was missing, causing a potential syntax error
            return false;
        },

        stop: function(n_clicks){
            stop_sequence();
            lastPauseTime = 0;
            return n_clicks;
        },

        updateFigure: function(data, timestamp_n_events, timestamp_event) {
            // Validate the presence of essential data
            if (!data) {
                return null; // or provide a default empty plot configuration
            }

            // Initialize variables for constructing the plot
            var highlightColor = '#FFD700'; // Gold color for potential highlighting
            var defaultMarkerColor = 'rgba(158,202,225,0.5)';
            var timestamp = timestamp_event && timestamp_event["srcElement.value"] ? timestamp_event["srcElement.value"] : null;

            // Prepare data arrays
            const timeValues = Object.values(data.time);

            // Find the index of the timestamp in the data, if a valid timestamp is provided
            const index = timestamp ? timeValues.indexOf(timestamp) : -1;

            // Construct traces
            var candlestickTrace = {
                type: 'candlestick',
                x: timeValues,
                close: Object.values(data.close),
                high: Object.values(data.high),
                low: Object.values(data.low),
                open: Object.values(data.open),
                increasing: {line: {color: '#17BECF'}},
                decreasing: {line: {color: '#7F7F7F'}},
                yaxis: 'y'
            };

            var volumeTrace = {
                type: 'bar',
                x: timeValues,
                y: Object.values(data.volume),
                marker: {
                    color: timeValues.map((_, i) => i === index ? highlightColor : defaultMarkerColor),
                },
                yaxis: 'y2'
            };

            // Define the layout
            var layout = {
                xaxis: { autorange: true, title: 'Time' },
                yaxis: { title: `${data.base} price [${data.quote}]`, side: 'left', autorange: true },
                yaxis2: { title: `${data.base} volume [${data.base}]`, overlaying: 'y', side: 'right', autorange: true },
                dragmode: 'zoom',
                margin: { l: 50, r: 50, t: 35, b: 35 },
                showlegend: false
            };

            // Construct and return the plot configuration
            return {
                data: [candlestickTrace, volumeTrace],
                layout: layout
            };
        }


    }
})




// changeInstrument('https://surikov.github.io/webaudiofontdata/sound/0290_Aspirin_sf2_file.js','_tone_0290_Aspirin_sf2_file');



