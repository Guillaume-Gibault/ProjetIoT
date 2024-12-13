import time
import pyb

# Liste des fréquences des notes en Hz
NOTES = {
    'A3F': 208,
    'B3F': 233,
    'B3': 247,
    'C4': 261,
    'C4S': 277,
    'D4': 294,
    'E4': 330,
    'E4F': 311,
    'F4': 349,
    'G4': 392,
    'A4': 440,
    'A4F': 415,
    'B4F': 466,
    'B4': 493,
    'C5': 523,
    'C5S': 554,
    'D5': 587,
    'DS5': 622,
    'E5': 659,
    'E5F': 622,
    'F5': 698,
    'F5S': 740,
    'G5': 784,
    'A5': 880,
    'A5F': 831,
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
    ('C5S', 0.6), ('E5F', 1.0), ('E5F', 0.6), ('F5', 0.6), ('A5F', 0.1), ('F5S', 0.1), ('F5', 0.1), ('E5F', 0.1),
    ('C5S', 0.6), ('E5F', 1.0), ('REST', 0.4), ('A4F', 0.2), ('A4F', 1.0),
    ('REST', 0.2), ('C4S', 0.1), ('C4S', 0.1), ('C4S', 0.1), ('C4S', 0.1), ('E4F', 0.2),
    ('REST', 0.1), ('C4', 0.1), ('B3F', 0.1), ('A3F', 0.5),
    ('REST', 0.1), ('B3F', 0.1), ('B3F', 0.1), ('C4', 0.1), ('C4S', 0.3),
    ('A3F', 0.1), ('A4F', 0.2), ('A4F', 0.1), ('E4F', 0.5),
    ('REST', 0.1), ('B3F', 0.1), ('B3F', 0.1), ('C4', 0.1), ('C4S', 0.1), ('B3F', 0.1),
    ('C4S', 0.2), ('E4F', 0.1), ('REST', 0.1), ('C4', 0.1), ('B3F', 0.1), ('B3F', 0.1), ('A3F', 0.3),
    ('REST', 0.1), ('B3F', 0.1), ('B3F', 0.1), ('C4', 0.1), ('C4S', 0.1), ('A3F', 0.1),
    ('A3F', 0.1), ('E4F', 0.1), ('E4F', 0.1), ('E4F', 0.1), ('F4', 0.4), ('E4F', 0.5),
    ('C4S', 0.5), ('E4F', 0.1), ('F4', 0.1), ('C4S', 0.1), ('E4F', 0.1), ('E4F', 0.1), ('E4F', 0.1), ('F4', 0.1),
    ('E4F', 0.2), ('A3F', 0.2), ('REST', 0.2), ('B3F', 0.1), ('C4', 0.1), ('C4S', 0.1), ('A3F', 0.3),
    ('REST', 0.1), ('E4F', 0.1), ('F4', 0.1), ('E4F', 0.3),
    ('B4F', 0.4), ('B4F', 0.4), ('A4F', 0.4), ('A4F', 0.4),
    ('F5', 0.6), ('F5', 0.6), ('E5F', 1.0), ('B4F', 0.4),
    ('B4F', 0.4), ('A4F', 0.4), ('A4F', 0.6), ('E5F', 0.6),
    ('C5S', 0.6), ('C5', 0.6), ('B4F', 0.4), ('C5S', 0.6),
    ('C5S', 0.6), ('C5S', 0.6), ('C5S', 0.6), ('E5F', 0.6), ('C5', 0.6),
    ('B4F', 0.4), ('A4F', 0.4), ('A4F', 0.4), ('A4F', 0.6), ('E5F', 0.6),
    ('C5S', 0.6), ('B4F', 0.4), ('B4F', 0.4), ('A4F', 0.4), ('A4F', 0.6)
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
    for note, duration in MELODY_1:
        play_tone(note, duration)
        time.sleep(SHORT_PAUSE)
    time.sleep(2)  # Pause entre les deux mélodies
    for note, duration in MELODY_2:
        play_tone(note, duration)
        time.sleep(SHORT_PAUSE)
except KeyboardInterrupt:
    print("Arrêt de la lecture.")
    tim1 = pyb.Timer(1, freq=NOTES[note])  # Configuration du timer 1 pour la génération de la PWM
    pwm = tim1.channel(1, pyb.Timer.PWM, pin=d6)  # Configuration de la PWM pour la broche D6
    pwm.pulse_width_percent(0)
    tim1.deinit()  # Arrêter le timer
print("Fin de la mélodie.")
