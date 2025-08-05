import io
from mido import Message, MidiFile, MidiTrack, MetaMessage

def create_midi_file(grids, notes, beats, instruments, bpm=120):
    mid = MidiFile(type=1)
    mid.ticks_per_beat = 480

    for t, grid in enumerate(grids):
        track = MidiTrack()
        mid.tracks.append(track)
        # Set instrument (program change)
        track.append(MetaMessage('track_name', name=f'Track {t+1}', time=0))
        track.append(Message('program_change', program=instruments[t], time=0))
        if t == 0:
            # Add tempo to the first track
            tempo = int(60_000_000 / bpm)
            track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
        for beat in range(beats):
            for i, note in enumerate(notes):
                if grid[i][beat]:
                    track.append(Message('note_on', note=note, velocity=64, time=0))
                    track.append(Message('note_off', note=note, velocity=64, time=480))
            if not any(grid[i][beat] for i in range(len(notes))):
                track.append(Message('note_off', note=0, velocity=0, time=480))
        track.append(MetaMessage('end_of_track', time=0))

    buf = io.BytesIO()
    mid.save(file=buf)
    buf.seek(0)
    return buf
