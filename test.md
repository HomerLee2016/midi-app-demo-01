# MIDI Grid Sequencer

A simple web-based MIDI sequencer built with Flask. It provides a grid interface (notes C3–C4 over 4 beats) where you can toggle cells on/off, play the sequence in-browser, and save it as a MIDI file.

---

## Project Structure
```plaintext
midi_sequencer/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # HTML template for the grid UI
└── static/
    ├── style.css       # Grid and UI styling
    └── script.js       # Client-side grid logic, playback, and MIDI download
```

---

## 1. app.py
```python
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
``` 

---

## 2. requirements.txt
```plaintext
Flask
mido
python-rtmidi  # MIDI backend
```

---

## 3. templates/index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Grid MIDI Sequencer</title>
  <link rel="stylesheet" href="/static/style.css">
  <!-- Tone.js for in-browser playback -->
  <script src="https://cdn.jsdelivr.net/npm/tone@14.7.77/build/Tone.js"></script>
</head>
<body>
  <h1>Grid MIDI Sequencer</h1>
  <div id="grid">
    {% for note in notes %}
    <div class="row">
      <div class="label">{{ note }}</div>
      {% for _ in range(beats) %}
      <div class="cell"></div>
      {% endfor %}
    </div>
    {% endfor %}
  </div>
  <div class="controls">
    <button id="playBtn">Play</button>
    <button id="saveBtn">Save as MIDI</button>
  </div>
  <script src="/static/script.js"></script>
</body>
</html>
```

---

## 4. static/style.css
```css
body {
  font-family: Arial, sans-serif;
  padding: 20px;
}
#grid { display: inline-block; }
.row { display: flex; }
.label {
  width: 50px;
  line-height: 30px;
}
.cell {
  width: 30px;
  height: 30px;
  margin: 2px;
  border: 1px solid #ccc;
  background: #fff;
  cursor: pointer;
}
.cell.active { background: #4caf50; }
.controls {
  margin-top: 20px;
}
.controls button {
  padding: 10px 20px;
  margin-right: 10px;
  font-size: 16px;
}
```  

---

## 5. static/script.js
```javascript
document.addEventListener('DOMContentLoaded', () => {
  const notes = [48,49,50,51,52,53,54,55,56,57,58,59,60]; // MIDI note numbers
  const cells = document.querySelectorAll('.cell');

  // Toggle cells
  cells.forEach(cell => cell.addEventListener('click', () => cell.classList.toggle('active')));

  // Collect grid state
  function getGrid() {
    return Array.from(document.querySelectorAll('.row')).map(row => 
      Array.from(row.querySelectorAll('.cell')).map(c => c.classList.contains('active') ? 1 : 0)
    );
  }

  // Play sequence using Tone.js
  document.getElementById('playBtn').addEventListener('click', async () => {
    await Tone.start();
    const synth = new Tone.PolySynth(Tone.Synth).toDestination();
    const grid = getGrid();
    const now = Tone.now();
    const beatDuration = 0.5; // 0.5s per beat (120 BPM)

    grid.forEach((row, i) => {
      row.forEach((active, beat) => {
        if (active) {
          synth.triggerAttackRelease(
            Tone.Frequency(notes[i], 'midi'),
            beatDuration,
            now + beat * beatDuration
          );
        }
      });
    });
  });

  // Save as MIDI
  document.getElementById('saveBtn').addEventListener('click', () => {
    fetch('/save', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ grid: getGrid() })
    })
    .then(res => res.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = 'sequence.mid';
      a.click(); URL.revokeObjectURL(url);
    });
  });
});
```
