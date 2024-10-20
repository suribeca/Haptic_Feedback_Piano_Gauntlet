import mido

# Diccionario para conversión a notación conocida
notas_latinas = ['Do', 'Do♯', 'Re', 'Re♯', 'Mi', 'Fa', 'Fa♯', 'Sol', 'Sol♯', 'La', 'La♯', 'Si']

# Conversor de nota MIDI a nota conocida
def conversion_nota(numero_midi):
    # Calcular la octava y el semitono
    semitono = numero_midi % 12
    octava = (numero_midi // 12) - 1  # MIDI 0 es en octava -1
    
    # Obtener la nota y la octava en notación latina
    nota = notas_latinas[semitono] 
    return f"{nota}{octava}"


# Función para cargar las notas de un archivo MIDI
def cargar_notas_midi(archivo_midi):
    midi = mido.MidiFile(archivo_midi)
    notas = []
    
    for mensaje in midi:
        # Solo capturamos eventos 'note_on' con velocidad > 0
        if mensaje.type == 'note_on' and mensaje.velocity > 0:
            notas.append(mensaje.note)
    return notas

# Función para comparar las notas tocadas con las del archivo MIDI
def comparar_notas(notas_esperadas, input_port_name):
    tocadas = []
    indice = 0
    total_notas = len(notas_esperadas)
    
    print(f"Debes tocar las siguientes {total_notas} notas en el orden correcto.")
    
    # Abrimos el puerto de entrada MIDI para capturar las notas
    with mido.open_input(input_port_name) as inport:
        for msg in inport:
            if msg.type == 'note_on' and msg.velocity > 0:
                nota = msg.note
                nota_trad = conversion_nota(nota)
                tocadas.append(nota)
                print(f"Tocaste: {nota_trad}")
                
                # Comparar la nota tocada con la esperada
                if nota == notas_esperadas[indice]:
                    print(f"Correcto! Nota {nota_trad} coincide con la esperada.")
                    indice += 1
                else:
                    print(f"Error: tocaste {nota_trad}, pero se esperaba {notas_esperadas[indice]}.")
                    break
                
                # Si hemos llegado al final de las notas esperadas
                if indice >= total_notas:
                    print("¡Felicitaciones! Tocaste todas las notas en el orden correcto.")
                    break

# Nombre del archivo MIDI de entrada
archivo_midi = 'Midi2.mid'

# Cargar las notas desde el archivo MIDI
notas_esperadas = cargar_notas_midi(archivo_midi)
notas_trad = []
for nota in notas_esperadas:
    notas_trad.append(conversion_nota(nota))
print(f"Notas esperadas: {notas_trad}")

#Detectar y Buscar nombre del piano MIDI
print(mido.get_input_names())

# Nombre del puerto MIDI de tu teclado, reemplazar por lo que se encuentre en la impresión anterior
input_port_name = 'AKM320 0'

# Comparar las notas tocadas con las notas del archivo MIDI
comparar_notas(notas_esperadas, input_port_name)
