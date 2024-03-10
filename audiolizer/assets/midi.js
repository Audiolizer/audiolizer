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
    // Assuming 'timestamp' is the value you want to communicate to Dash
    document.getElementById('timestamp-trigger').value = timestamp;

    // Optionally, trigger an input event to ensure Dash detects the change
    var event = new Event('input', { bubbles: true });
    document.getElementById('timestamp-trigger').dispatchEvent(event);
}



function play_sequence(preset, notes){
    window['envelope'] = [];
    window['timeoutIDs'] = [];

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


window.dash_clientside = Object.assign({}, window.dash_clientside, {
    dash_midi: {
        play: function(n_clicks, preset, path, notes) {
            // stop any currently playing sequence
            stop_sequence();
            if (typeof window[preset] !== 'undefined') {
                console.log('variable ' + preset + ' exists!');
                play_sequence(preset, notes);
            } else {
            console.log('loading '+ preset + ' from ' + path);
            player.loader.startLoad(audioContext, path, preset);
            player.loader.waitLoad(function () {
                instr=window[preset];
                play_sequence(preset, notes);
            return false;
            });
            }
        },
        stop: function(n_clicks){
            stop_sequence();
            return n_clicks
        },
        highlight: function(timestamp) {
            if (!timestamp) {
                return window.dash_clientside.no_update; // Return no_update if no timestamp
            }

            // Example: Assuming your timestamp directly maps to the x-value of the candlestick data
            // You would need to replace this logic with whatever correctly identifies the point(s) to highlight based on your timestamp and data structure
            
            // This is a placeholder for how you might structure the selectedData based on your application's requirements
            const selectedData = {
                points: [{
                    x: timestamp, // The x-value (timestamp) of the data point to highlight
                    // Additional properties as needed to match the structure expected by your chart configuration
                }]
            };

            return selectedData;
        },

    }
})




// changeInstrument('https://surikov.github.io/webaudiofontdata/sound/0290_Aspirin_sf2_file.js','_tone_0290_Aspirin_sf2_file');



