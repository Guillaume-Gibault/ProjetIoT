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
    'CS5': 554,
    'D5': 587,
    'DS5': 622,
    'E5': 659,
    'F5': 698,
    'FS5': 740,
    'G5': 784,
    'A5': 880,
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
    ('D5', 0.45), ('E5', 0.45), ('A4', 0.3),
    ('E5', 0.45), ('FS5', 0.45), ('A5', 0.15), ('G5', 0.15), ('FS5', 0.3),
    ('D5', 0.45), ('E5', 0.45), ('A4', 0.6),
    ('A4', 0.15), ('A4', 0.15), ('B4', 0.15), ('D5', 0.3), ('D5', 0.15),
    ('D5', 0.45), ('E5', 0.45), ('A4', 0.3),
    ('E5', 0.45), ('FS5', 0.45), ('A5', 0.15), ('G5', 0.15), ('FS5', 0.3),
    ('D5', 0.45), ('E5', 0.45), ('A4', 0.6),
    ('A4', 0.15), ('A4', 0.15), ('B4', 0.15), ('D5', 0.3), ('D5', 0.15),
    ('REST', 0.3), ('B4', 0.15), ('CS5', 0.15), ('D5', 0.15), ('D5', 0.15), ('E5', 0.15), ('CS5', 0.225),
    ('B4', 0.075), ('A4', 0.6), ('REST', 0.3),
    ('REST', 0.15), ('B4', 0.15), ('B4', 0.15), ('CS5', 0.15), ('D5', 0.15), ('B4', 0.3), ('A4', 0.15),
    ('A5', 0.15), ('REST', 0.15), ('A5', 0.15), ('E5', 0.45), ('REST', 0.3),
    ('B4', 0.15), ('B4', 0.15), ('CS5', 0.15), ('D5', 0.15), ('B4', 0.15), ('D5', 0.15), ('E5', 0.15), ('REST', 0.15),
    ('REST', 0.15), ('CS5', 0.15), ('B4', 0.15), ('A4', 0.45), ('REST', 0.3),
    ('REST', 0.15), ('B4', 0.15), ('B4', 0.15), ('CS5', 0.15), ('D5', 0.15), ('B4', 0.15), ('A4', 0.3),
    ('E5', 0.15), ('E5', 0.15), ('E5', 0.15), ('FS5', 0.15), ('E5', 0.3), ('REST', 0.3)
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
