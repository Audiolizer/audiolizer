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


var isPlaying = false; // Tracks if the sequence is currently playing
var audioContextTimeAtStart = 0; // When the playback was started
var lastPauseTime = 0; // When the playback was paused

function updateTimestampStore(timestamp, when_, offset_, lastPauseTime_) {
    const timestampInputElement = document.getElementById('timestamp-input');
    timestampInputElement.value = timestamp; // Update the value

    // Manually trigger a "change" event for the input element
    var timestampEvent = new Event('change', { 'bubbles': true });
    timestampInputElement.dispatchEvent(timestampEvent);

    const whenInputElement = document.getElementById('when-input');
    whenInputElement.value = when_;

    const offsetInputElement = document.getElementById('offset-input');
    offsetInputElement.value = offset_;

    const lastPauseInputElement = document.getElementById('lastPauseTime-input');
    lastPauseInputElement.value = lastPauseTime_;
}



function play_sequence(preset, notes, startFrom = 0) {
    window['envelope'] = [];
    window['timeoutIDs'] = [];
    audioContextTimeAtStart = audioContext.currentTime;

    const scheduleNote = (t, when, pitch, duration, volume, offset, isLast) => {
        var timeoutID = setTimeout(() => {
            // Here we log the current timestamp, audioContext's current time, and the 'when' value
            // console.log(`Timestamp: ${t}, AudioContext CurrentTime: ${audioContext.currentTime}, When: ${when}`);
            if (isLast) {
                lastPauseTime = 0;
                // console.log('Stopped at end of sequence: ', lastPauseTime, 'seconds');
                const lastPauseInputElement = document.getElementById('lastPauseTime-input');
                lastPauseInputElement.value = lastPauseTime;
                isPlaying = false;
            } else {
                lastPauseTime = offset;
            }
            updateTimestampStore(t, when, offset, lastPauseTime);
        }, when * 1000); // Convert 'when' to milliseconds
        window['timeoutIDs'].push(timeoutID);
    };


    for (var n = 0; n < notes['when'].length; n++) {
        t = notes['t'][n]
        when = notes['when'][n];
        pitch = notes['pitch'][n];
        duration = notes['duration'][n];
        volume = notes['volume'][n];
        isLast = (notes['when'].length > 1) && (n == notes['when'].length - 1);

        if (when >= startFrom) {
            // Schedule each note by calling the function that creates a closure
            scheduleNote(t, when - startFrom, pitch, duration, volume, when, isLast);

            var envelope = player.queueWaveTable(
                audioContext,
                audioContext.destination,
                window[preset],
                audioContext.currentTime + when - startFrom,
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
    if (typeof window['envelope'] !== 'undefined' && Array.isArray(window['envelope'])) {
        window['envelope'].forEach(function(envelope) {
            // Check if envelope is an object and has a cancel method before calling it
            if (envelope && typeof envelope.cancel === 'function') {
                envelope.cancel();
            } else {
                console.log('Attempted to cancel an invalid envelope');
            }
        });
        window['envelope'] = []; // Clear the envelopes array after stopping
    } else {
        console.log('No envelopes to cancel or envelope array is undefined');
    }

    // Clear all scheduled setTimeout calls to prevent logging
    if (typeof window['timeoutIDs'] !== 'undefined' && Array.isArray(window['timeoutIDs'])) {
        window['timeoutIDs'].forEach(function(timeoutID) {
            clearTimeout(timeoutID);
        });
        window['timeoutIDs'] = []; // Clear the timeoutIDs array after clearing timeouts
    } else {
        console.log('No scheduled logs to cancel or timeoutIDs array is undefined');
    }
}



function loadAndPlaySequence(preset, path, notes, startFrom) {
    if (typeof window[preset] !== 'undefined') {
        // console.log('Variable ' + preset + ' exists!');
        play_sequence(preset, notes, startFrom);
    } else {
        // console.log('Loading ' + preset + ' from ' + path);
        player.loader.startLoad(audioContext, path, preset);
        player.loader.waitLoad(function() {
            instr = window[preset];
            play_sequence(preset, notes, startFrom);
        });
    }
}

function findClosestBeepIndex(notes, targetTimestamp) {
    let closestBeepIndex = -1;
    // Ensure targetTimestamp is a string to safely use .includes()
    let targetTimeString = String(targetTimestamp);

    if (targetTimestamp.includes(':')) {
        // convert from 2024-03-30 10:15 to 2024-03-30T10:15:00
        targetTimeString = targetTimeString.replace(' ', 'T') + ':00';
    }

    // let clickTimestamp = new Date(clickData.points[0].x.replace(' ', 'T') + ':00');
    // Standardize the target timestamp to include a time part, if missing
    if (!targetTimeString.includes('T')) {
        targetTimeString += "T00:00:00";
    }
    let targetTime = new Date(targetTimeString);

    for (let i = notes['t'].length - 1; i >= 0; i--) {
        let noteTimestamp = new Date(notes['t'][i]);
        if (noteTimestamp <= targetTime) {
            closestBeepIndex = i;
            break;
        }
    }

    return closestBeepIndex;
}



window.dash_clientside = Object.assign({}, window.dash_clientside, {
    dash_midi: {
        play: function(n_clicks, preset, path, notes) {
            if (n_clicks > 0) { // Check if n_clicks is greater than 0
                if (!isPlaying) {
                    loadAndPlaySequence(preset, path, notes, lastPauseTime);
                    isPlaying = true;
                } else {
                    isPlaying = false;
                }
            }
            return false;
        },

        playFromSelect: function(selectData, preset, path, notes) {
            let pointIndexStart = null;
            let pointIndexEnd = null;
            const selectDataString = JSON.stringify(selectData);
            let start = 0;
            // Check if selectData and selectData.points exist and have at least one point
            if (selectData && selectData.points && selectData.points.length > 0) {
                stop_sequence();
                let selectStartTime = selectData.points[0].x;
                let selectEndTime = selectData.points[selectData.points.length - 1].x;

                // Convert selectData to a JSON string (if needed for other purposes)
                // Safely access the pointIndex of the first and last points
                pointIndexStart = findClosestBeepIndex(notes, selectStartTime);
                pointIndexEnd = findClosestBeepIndex(notes, selectEndTime);

                // Construct a new notes object with notes ranging from pointIndexStart to pointIndexEnd
                let selectedNotes = {
                    't': [],
                    'when': [],
                    'pitch': [],
                    'duration': [],
                    'volume': [],
                    // Add any other necessary properties following the same pattern
                };

                // Iterate from pointIndexStart to pointIndexEnd to fill selectedNotes
                for (let i = pointIndexStart; i <= pointIndexEnd; i++) {
                    selectedNotes['t'].push(notes['t'][i]);
                    selectedNotes['when'].push(notes['when'][i]);
                    selectedNotes['pitch'].push(notes['pitch'][i]);
                    selectedNotes['duration'].push(notes['duration'][i]);
                    selectedNotes['volume'].push(notes['volume'][i]);
                    // Add any other necessary properties in the same way
                }

                start = selectedNotes['when'][0];

                lastPauseTime = start;
                // console.log("PLAY FROM SELECT, selectedNotes:", selectedNotes, "starting at", start);
                loadAndPlaySequence(preset, path, selectedNotes, start); // Ensure you pass selectedNotes here
                isPlaying = true;
            } else {
                // Handle the case where selectData is null or points key doesn't exist
                // console.log('No points data available in selectData.');
            }

            // Return pointIndex. Replace this with the appropriate Dash component update as needed
            return selectDataString + JSON.stringify({start: pointIndexStart, end: pointIndexEnd});
        },

        playFromClick: function(clickData, preset, path, notes) {
            let pointIndex = null;
            const clickDataString = JSON.stringify(clickData);
            console.log(clickDataString);
            stop_sequence();
            let start = 0;

            // Check if clickData and clickData.points exist and have at least one point
            if (clickData && clickData.points && clickData.points.length > 0) {
                // Assuming clickData.points[0].x is '2024-03-30 09:30'
                let clickTimestamp = clickData.points[0].x;
                let closestBeepIndex = findClosestBeepIndex(notes, clickTimestamp);
                start = notes['when'][closestBeepIndex];
                lastPauseTime = start;
                loadAndPlaySequence(preset, path, notes, start);
                isPlaying = true;
            } else {
                // Handle the case where clickData is null or points key doesn't exist
                console.log('No points data available in clickData.');
            }

            // Return pointIndex. Replace this with the appropriate Dash component update as needed
            return clickDataString
        },

        playOnHover: function(hoverData, preset, path, notes) {
            // Before playing, ensure the AudioContext is running
            if (audioContext.state === 'suspended') {
                audioContext.resume().then(() => {
                    console.log("AudioContext resumed successfully");
                });
                return;
            }
            const hoverDataString = JSON.stringify(hoverData);

            if (!isPlaying) {
                console.log('not playing, proceeding onHover');
                stop_sequence();

                if (hoverData && hoverData.points && hoverData.points.length > 0) {
                    // Assuming hoverData.points[0].x is the timestamp on the chart
                    let hoverTimestamp = hoverData.points[0].x;

                    let closestBeepIndex = findClosestBeepIndex(notes, hoverTimestamp);

                    if (closestBeepIndex !== -1) {
                        let singleNote = {
                            't': [notes['t'][closestBeepIndex]],
                            'when': [notes['when'][closestBeepIndex]],
                            'pitch': [notes['pitch'][closestBeepIndex]],
                            'duration': [notes['duration'][closestBeepIndex]],
                            'volume': [notes['volume'][closestBeepIndex]],  // Assuming volume is a parameter your system uses
                        };

                        let start = singleNote['when'][0];
                        lastPauseTime = start;
                        loadAndPlaySequence(preset, path, singleNote, start);
                        isPlaying = false;  // Ensure you correctly manage this flag in your actual code
                    } else {
                        console.log('No corresponding beep found for hover timestamp.');
                        console.log('hover data', hoverDataString);
                        console.log('notes range', notes['t']);
                    }
                } else {
                    console.log('No points data available in hoverData.');
                }
            } else {
                console.log("already playing, preventing onHover playback");
            }
        },


        pause: function(n_clicks){
            stop_sequence();
            isPlaying = false;
            console.log('Paused at: ', lastPauseTime, 'seconds');
  
            return n_clicks;

        },

        stop: function(n_clicks){
            stop_sequence();
            lastPauseTime = 0;
            console.log('Stopped at: ', lastPauseTime, 'seconds');
            const lastPauseInputElement = document.getElementById('lastPauseTime-input');
            lastPauseInputElement.value = lastPauseTime;
            isPlaying = false;

            return n_clicks;
        },

        updateFigure: function(incomingData, timestamp_n_events, timestamp_event) {
            // Validate the presence of essential data
            if (!incomingData) {
                console.error("No data provided, skipping update.");
                return;
            }

            // Initialize variables for constructing the plot
            var highlightColor = '#FFD700'; // Gold color for potential highlighting
            var defaultMarkerColor = 'rgba(158,202,225,0.5)';
            var timestamp = timestamp_event && timestamp_event["srcElement.value"] ? timestamp_event["srcElement.value"] : null;

            // Prepare data arrays
            const timeValues = Object.values(incomingData.time);

            // Find the index of the timestamp in the data, if a valid timestamp is provided
            const index = timestamp ? timeValues.indexOf(timestamp) : -1;

            var traces = [{
                type: 'candlestick',
                x: timeValues,
                close: Object.values(incomingData.close),
                high: Object.values(incomingData.high),
                low: Object.values(incomingData.low),
                open: Object.values(incomingData.open),
                increasing: {line: {color: '#17BECF'}},
                decreasing: {line: {color: '#7F7F7F'}},
                yaxis: 'y'
            }, {
                type: 'bar',
                x: timeValues,
                y: Object.values(incomingData.volume),
                marker: {
                    color: timeValues.map((_, i) => i === index ? highlightColor : defaultMarkerColor),
                },
                yaxis: 'y2'
            }];

            var layout = {
                xaxis: {
                    autorange: true,
                    title: 'Time',
                    gridcolor: '#444444',  // Darker lines for the grid
                    tickcolor: '#d4d4d4'  // Light grey ticks to match the text
                 },
                yaxis: {
                    title: `${incomingData.base} price [${incomingData.quote}]`,
                    side: 'left',
                    autorange: true,
                    gridcolor: '#444444',
                    tickcolor: '#d4d4d4'
                },
                yaxis2: {
                    title: `${incomingData.base} volume [${incomingData.base}]`,
                    overlaying: 'y',
                    side: 'right',
                    autorange: true,
                    gridcolor: '#444444',
                    tickcolor: '#d4d4d4'
                },
                dragmode: 'select',
                hovermode: 'x',
                margin: { l: 50, r: 50, t: 35, b: 35 },
                showlegend: false,
                paper_bgcolor: '#1e1e1e',  // Dark background for the outer area
                plot_bgcolor: '#1e1e1e',  // Dark background for the plotting area
                font: {
                    color: '#d4d4d4'  // Light grey text for better readability on dark background
                },
            };

            // Construct and return the plot configuration
            return {
                data: traces,
                layout: layout
            };

        }



    }
})




// changeInstrument('https://surikov.github.io/webaudiofontdata/sound/0290_Aspirin_sf2_file.js','_tone_0290_Aspirin_sf2_file');



