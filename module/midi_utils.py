import io
from mido import Message, MidiFile, MidiTrack, MetaMessage

def create_midi_file(grid, notes, beats):
    mid = MidiFile(type=1)
    track = MidiTrack()
    mid.tracks.append(track)

    # Add track name
    track.append(MetaMessage('track_name', name='Sequencer', time=0))
    mid.ticks_per_beat = 480

    # Build note events
    for beat in range(beats):
        for i, note in enumerate(notes):
            if grid[i][beat]:
                track.append(Message('note_on', note=note, velocity=64, time=0))
                track.append(Message('note_off', note=note, velocity=64, time=480))
        # Insert silent tick if no notes to advance time
        if not any(grid[i][beat] for i in range(len(notes))):
            track.append(Message('note_off', note=0, velocity=0, time=480))

    # End of track
    track.append(MetaMessage('end_of_track', time=0))

    # Write to in-memory bytes buffer
    buf = io.BytesIO()
    mid.save(file=buf)
    buf.seek(0)
    return buf
