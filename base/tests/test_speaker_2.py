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
    'REST': 20  # Silence
}

# Durées des notes
NOTE_DURATION = 0.3  # Durée standard d'une note
SHORT_PAUSE = 0.05   # Pause courte entre les notes

# Partition de "Funky Town"
MELODY_1 = [
    ('G4', 0.1), ('REST', 0.05), ('G4', 0.1), ('REST', 0.05),
    ('F4', 0.1), ('REST', 0.05), ('G4', 0.3), ('REST', 0.05),
    ('D4', 0.3), ('REST', 0.05), ('D4', 0.1), ('REST', 0.05),
    ('G4', 0.1), ('REST', 0.05), ('C5', 0.1), ('REST', 0.05),
    ('B4', 0.1), ('REST', 0.05), ('G4', 0.2)
]

# Partition de "Never Gonna Give You Up"
MELODY_2 = [
    ('D4', 0.3), ('E4', 0.3), ('F4', 0.3), ('G4', 0.3),
    ('A4', 0.3), ('B4', 0.3), ('C5', 0.3), ('D5', 0.3),
    ('E5', 0.3), ('F5', 0.3), ('G5', 0.3), ('A5', 0.3),
    ('B5', 0.3), ('C6', 0.3), ('D6', 0.3), ('E6', 0.3),
    ('F6', 0.3), ('G6', 0.3), ('A6', 0.3), ('B6', 0.3),
    ('C7', 0.3), ('D7', 0.3), ('E7', 0.3), ('F7', 0.3),
    ('G7', 0.3), ('A7', 0.3), ('B7', 0.3), ('C8', 0.3),
    ('REST', 0.3), ('C8', 0.3), ('B7', 0.3), ('A7', 0.3),
    ('G7', 0.3), ('F7', 0.3), ('E7', 0.3), ('D7', 0.3),
    ('C7', 0.3), ('B6', 0.3), ('A6', 0.3), ('G6', 0.3),
    ('F6', 0.3), ('E6', 0.3), ('D6', 0.3), ('C6', 0.3),
    ('B5', 0.3), ('A5', 0.3), ('G5', 0.3), ('F5', 0.3),
    ('E5', 0.3), ('D5', 0.3), ('C5', 0.3), ('B4', 0.3),
    ('A4', 0.3), ('G4', 0.3), ('F4', 0.3), ('E4', 0.3),
    ('D4', 0.3), ('C4', 0.3), ('B3', 0.3), ('A3', 0.3),
    ('G3', 0.3), ('F3', 0.3), ('E3', 0.3), ('D3', 0.3),
    ('C3', 0.3), ('B2', 0.3), ('A2', 0.3), ('G2', 0.3),
    ('F2', 0.3), ('E2', 0.3), ('D2', 0.3), ('C2', 0.3),
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
    for note, duration in [MELODY_1, MELODY_2]:
        play_tone(note, duration)
        time.sleep(SHORT_PAUSE)
except KeyboardInterrupt:
    print("Arrêt de la lecture.")
    tim1 = pyb.Timer(1, freq=NOTES[note])  # Configuration du timer 1 pour la génération de la PWM
    pwm = tim1.channel(1, pyb.Timer.PWM, pin=d6)  # Configuration de la PWM pour la broche D6
    pwm.pulse_width_percent(0)
    tim1.deinit()  # Arrêter le timer
print("Fin de la mélodie.")
