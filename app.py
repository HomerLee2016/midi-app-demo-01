from flask import Flask, render_template, request, send_file
from module.midi_utils import create_midi_file
from module.keyboard_utils import render_keyboard

app = Flask(__name__)

# Notes C3 to C4 (MIDI numbers 48–60)
NOTES = list(range(48, 61))
DEFAULT_BARS = 2
DEFAULT_BEATS = DEFAULT_BARS * 4

INSTRUMENT_OPTIONS = [
    {"name": "Piano", "midi": 0, "tone": "piano"},
    {"name": "Violin", "midi": 40, "tone": "violin"},
    {"name": "Guitar", "midi": 24, "tone": "guitar"},
    {"name": "Vocal Harmony", "midi": 52, "tone": "choir"}
]

@app.route('/')
def index():
    bpm = request.args.get('bpm', default=120, type=int)
    beats = request.args.get('beats', default=None, type=int)
    # Only use beats from query if present and valid, else use DEFAULT_BEATS
    if not beats or beats < 1:
        beats = DEFAULT_BEATS
    note_types = render_keyboard()
    return render_template(
        'index.html',
        note_types=note_types,
        beats=beats,
        beat_speed=bpm,
        bpm_label="♩",
        instrument_options=INSTRUMENT_OPTIONS,
        track1_instrument=0,  # default Piano
        track2_instrument=3   # default Vocal Harmony
    )

@app.route('/save', methods=['POST'])
def save_midi():
    data = request.json
    grids = data.get('grids')  # list of 2D lists
    instruments = data.get('instruments', [0, 52])  # MIDI program numbers
    beats = data.get('beats', DEFAULT_BEATS)  # get beats from client, default 8
    bpm = data.get('bpm', 120)  # get bpm from client, default 120

    # Pass bpm to MIDI creation
    buf = create_midi_file(grids, NOTES, beats, instruments, bpm)

    return send_file(
        buf,
        as_attachment=True,
        download_name='sequence.mid',
        mimetype='audio/midi'
    )

if __name__ == '__main__':
    app.run(debug=True)