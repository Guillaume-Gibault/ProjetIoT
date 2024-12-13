from machine import Pin, PWM
import time

# Configuration de la broche SIG en sortie PWM
speaker = PWM(Pin(15))  # Remplacez 15 par le numéro de votre broche
speaker.duty_u16(32768)  # Volume (50% duty cycle)

# Durées des notes
NOTE_DURATION = 0.3  # Durée standard d'une note
SHORT_PAUSE = 0.05   # Pause courte entre les notes

# Fréquences des notes en Hz
NOTES = {
    'C4': 262,
    'D4': 294,
    'E4': 330,
    'F4': 349,
    'G4': 392,
    'A4': 440,
    'B4': 494,
    'C5': 523,
    'D5': 587,
    'E5': 659,
    'REST': 0  # Silence
}

# Partition simplifiée de "Funky Town"
MELODY = [
    ('C4', NOTE_DURATION), ('D4', NOTE_DURATION), ('E4', NOTE_DURATION), ('G4', NOTE_DURATION),
    ('G4', NOTE_DURATION), ('A4', NOTE_DURATION), ('G4', NOTE_DURATION), ('E4', NOTE_DURATION),
    ('C4', NOTE_DURATION), ('D4', NOTE_DURATION), ('E4', NOTE_DURATION), ('C4', NOTE_DURATION),
    ('REST', SHORT_PAUSE),
    ('C4', NOTE_DURATION), ('D4', NOTE_DURATION), ('E4', NOTE_DURATION), ('G4', NOTE_DURATION),
    ('A4', NOTE_DURATION), ('G4', NOTE_DURATION), ('E4', NOTE_DURATION), ('C4', NOTE_DURATION),
]

def play_tone(note, duration):
    if note == 'REST':
        speaker.duty_u16(0)  # Couper le son pour un silence
    else:
        speaker.freq(NOTES[note])
        speaker.duty_u16(32768)  # Volume 50%
    time.sleep(duration)
    speaker.duty_u16(0)  # Pause après chaque note

print("Lecture de la mélodie 'Funky Town'")
for note, duration in MELODY:
    play_tone(note, duration)
    time.sleep(SHORT_PAUSE)

speaker.deinit()  # Arrêter le signal PWM
print("Fin de la mélodie")
