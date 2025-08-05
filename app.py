from flask import Flask, render_template, request, send_file
from module.midi_utils import create_midi_file
from module.keyboard_utils import render_keyboard

app = Flask(__name__)

# Notes C3 to C4 (MIDI numbers 48–60)
NOTES = list(range(48, 61))
BEATS = 32

@app.route('/')
def index():
    bpm = request.args.get('bpm', default=120, type=int)
    note_types = render_keyboard()
    # Pass the actual Unicode character for quarter note (♩)
    return render_template('index.html', note_types=note_types, beats=BEATS, beat_speed=bpm, bpm_label="\u2669")  # default BPM

@app.route('/save', methods=['POST'])
def save_midi():
    grid = request.json.get('grid')  # 2D list of 0/1

    # Use the extracted function to create MIDI file in memory
    buf = create_midi_file(grid, NOTES, BEATS)

    return send_file(
        buf,
        as_attachment=True,
        download_name='sequence.mid',
        mimetype='audio/midi'
    )

if __name__ == '__main__':
    app.run(debug=True)