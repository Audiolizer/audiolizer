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


function play_sequence(preset, notes){
    window['envelope'] = [];
    for (var n = 0; n < notes['when'].length; n++) {
        when = notes['when'][n];
        pitch = notes['pitch'][n];
        duration = notes['duration'][n];
        volume = notes['volume'][n];

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
    if (typeof window['envelope'] !== 'undefined'){
        console.log('stopping');
        for (var n = 0; n < window['envelope'].length; n++) {
            window['envelope'][n].cancel(); 
        } 
    } else {
        console.log('nothing to cancel');
    }

}

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    dash_midi: {
        play: function(preset, path, notes) {
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
    }
})




// changeInstrument('https://surikov.github.io/webaudiofontdata/sound/0290_Aspirin_sf2_file.js','_tone_0290_Aspirin_sf2_file');



