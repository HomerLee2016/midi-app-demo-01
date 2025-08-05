def render_keyboard():
    # MIDI notes 48-60: C3 to C4
    # White keys: C, D, E, F, G, A, B (0, 2, 4, 5, 7, 9, 11)
    # Black keys: C#, D#, F#, G#, A# (1, 3, 6, 8, 10)
    note_types = []
    for i in range(48, 61):
        note_in_octave = i % 12
        if note_in_octave in [1, 3, 6, 8, 10]:
            note_types.append('black')
        else:
            note_types.append('white')
    return note_types
