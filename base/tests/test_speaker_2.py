import time
import pyb

# Liste des fréquences des notes en Hz
NOTES = {
    'C4': 262,
    'D4': 294,
    'E4': 330,
    'F4': 349,
    'G4': 392,
    'A4': 440,
    'B4': 494,
    'C5': 523,
    'REST': 0  # Silence
}

# Durées des notes
NOTE_DURATION = 0.3  # Durée standard d'une note
SHORT_PAUSE = 0.05   # Pause courte entre les notes

# Partition simplifiée de "Funky Town"
MELODY = [
    ('C4', NOTE_DURATION), ('D4', NOTE_DURATION), ('E4', NOTE_DURATION), ('G4', NOTE_DURATION),
    ('G4', NOTE_DURATION), ('A4', NOTE_DURATION), ('G4', NOTE_DURATION), ('E4', NOTE_DURATION),
    ('C4', NOTE_DURATION), ('D4', NOTE_DURATION), ('E4', NOTE_DURATION), ('C4', NOTE_DURATION),
    ('REST', SHORT_PAUSE),
    ('C4', NOTE_DURATION), ('D4', NOTE_DURATION), ('E4', NOTE_DURATION), ('G4', NOTE_DURATION),
    ('A4', NOTE_DURATION), ('G4', NOTE_DURATION), ('E4', NOTE_DURATION), ('C4', NOTE_DURATION),
]

# Configuration de la broche D6 pour la sortie PWM
d6 = pyb.Pin('D6', pyb.Pin.OUT_PP)

# Fonction pour jouer une note avec une durée
def play_tone(note, duration):
    tim1 = pyb.Timer(1, freq=NOTES[note])  # Configuration du timer 1 pour la génération de la PWM
    pwm = tim1.channel(1, pyb.Timer.PWM, pin=d6)  # Configuration de la PWM pour la broche D6
    if note == 'REST':
        pwm.pulse_width_percent(0)  # Couper le son pour un silence
    else:
        pwm.pulse_width_percent(50)  # Volume à 50%
    time.sleep(duration)
    pwm.pulse_width_percent(0)  # Pause après chaque note

print("Lecture de la mélodie.")
try:
    for note, duration in MELODY:
        play_tone(note, duration)
        time.sleep(SHORT_PAUSE)
except KeyboardInterrupt:
    print("Arrêt de la lecture.")
    tim1 = pyb.Timer(1, freq=NOTES[note])  # Configuration du timer 1 pour la génération de la PWM
    pwm = tim1.channel(1, pyb.Timer.PWM, pin=d6)  # Configuration de la PWM pour la broche D6
    pwm.pulse_width_percent(0)
    tim1.deinit()  # Arrêter le timer
print("Fin de la mélodie.")
