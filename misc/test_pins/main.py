from machine import Pin

# Lister les pins disponibles
print("Liste des pins disponibles sur la STM32WB55 :")
for pin_name in dir(Pin):
    if not pin_name.startswith("_"):  # Ignorer les attributs privés
        print(pin_name)
