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
