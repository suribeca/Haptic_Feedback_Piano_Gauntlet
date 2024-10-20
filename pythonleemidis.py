#En terminal, ejecutar pip install mido python-rtmidi
import mido

# Función para convertir números de notas MIDI a nombres de notas
def note_to_name(note_number):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_name = note_names[note_number % 12]
    octave = note_number // 12  # MIDI comienza en C0
    return f'{note_name}{octave}'

# Función para agrupar mensajes de notas que suenan simultáneamente (acordes)
def detect_chords(track):
    chords = []
    active_notes = []
    current_time = 0  # Tiempo absoluto en ticks

    for msg in track:
        current_time += msg.time  # Sumar el tiempo desde el último mensaje
        if msg.type == 'note_on' and msg.velocity > 0:
            # Añadir la nota activa con su tiempo de inicio
            active_notes.append((msg.note, current_time))
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            # Identificar la nota que se apaga y calcular su duración
            note_off_time = current_time
            for note, start_time in active_notes:
                if note == msg.note:
                    duration = note_off_time - start_time
                    chords.append((start_time, duration, note))
                    active_notes.remove((note, start_time))
                    break
    return chords

# Abre el archivo MIDI
midi_file = mido.MidiFile('./Midi2.mid')

# Lee las notas del archivo MIDI
for i, track in enumerate(midi_file.tracks):
    print(f'Track {i}: {track.name}')
    chords = detect_chords(track)
    
    grouped_chords = []
    current_chord = []
    last_time = None
    
    for start_time, duration, note in chords:
        if last_time is None or abs(start_time - last_time) <= 10:  # Agrupa notas tocadas al mismo tiempo (ajusta el umbral según sea necesario)
            current_chord.append((note, start_time, duration))
        else:
            if current_chord:
                grouped_chords.append(current_chord)
            current_chord = [(note, start_time, duration)]
        last_time = start_time
    
    if current_chord:
        grouped_chords.append(current_chord)

    # Imprimir acordes detectados
    for chord in grouped_chords:
        notes_in_chord = [note_to_name(note[0]) for note in chord]
        chord_start_time = min(note[1] for note in chord)
        chord_duration = max(note[2] for note in chord)
        print(f'Acorde: {notes_in_chord}, Tiempo de inicio: {chord_start_time}, Duración: {chord_duration}')
