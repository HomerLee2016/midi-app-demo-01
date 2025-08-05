from flask import Flask, render_template, request, send_file
import io
from mido import Message, MidiFile, MidiTrack

app = Flask(__name__)

# Notes C3 to C4 (MIDI numbers 48–60)
NOTES = list(range(48, 61))
BEATS = 4

@app.route('/')
def index():
    note_names = ['C3','C#3','D3','D#3','E3','F3','F#3','G3','G#3','A3','A#3','B3','C4']
    return render_template('index.html', notes=note_names, beats=BEATS)

@app.route('/save', methods=['POST'])
def save_midi():
    grid = request.json.get('grid')  # 2D list of 0/1

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    mid.ticks_per_beat = 480

    for beat in range(BEATS):
        for i, note in enumerate(NOTES):
            if grid[i][beat]:
                track.append(Message('note_on', note=note, velocity=64, time=0))
                track.append(Message('note_off', note=note, velocity=64, time=480))
        if not any(grid[i][beat] for i in range(len(NOTES))):
            track.append(Message('note_off', note=0, velocity=0, time=480))

    buf = io.BytesIO()
    mid.save(buf)
    buf.seek(0)

    return send_file(buf,
                     as_attachment=True,
                     download_name='sequence.mid',
                     mimetype='audio/midi')

if __name__ == '__main__':
    app.run(debug=True)
