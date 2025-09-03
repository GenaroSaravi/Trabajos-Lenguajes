# piedra_papel_tijera.py 
# Juego simple contra la computadora: primera versión 
 
import random 
 
opciones = ["piedra", "papel", "tijera"] 
 
print("¡Bienvenido! Vamos a jugar a Piedra, Papel o Tijera.") 
print("Escribí tu jugada (piedra/papel/tijera).") 
 
ronda = 1 
puntos_usuario = 0 
puntos_pc = 0 
 
while ronda <= 3: 
    print(f"\nRonda {ronda}") 
    jugada_usuario = input("Tu jugada: ").strip().lower() 
 
    if jugada_usuario not in opciones: 
        print("Entrada no válida. Debe ser piedra, papel o tijera.")

        continue  # no cuenta la ronda si la entrada es inválida 
 
    jugada_pc = random.choice(opciones) 
    print(f"La computadora eligió: {jugada_pc}") 
 
    if jugada_usuario == jugada_pc: 
        print("Empate.") 
    elif ( 
        (jugada_usuario == "piedra" and jugada_pc == "tijera") or 
        (jugada_usuario == "papel" and jugada_pc == "piedra") or 
        (jugada_usuario == "tijera" and jugada_pc == "papel") 
    ): 
        print("¡Ganaste la ronda!") 
        puntos_usuario += 1 
    else: 
        print("Perdiste la ronda.") 
        puntos_pc += 1 
 
    ronda += 1 
 
print("\n=== Resultado final ===") 
print(f"Tus puntos: {puntos_usuario} | Puntos de la PC: {puntos_pc}")
 
if puntos_usuario > puntos_pc: 
    print("¡Ganaste el juego!") 
elif puntos_usuario < puntos_pc: 
    print("La computadora ganó el juego.") 
else: 
    print("Empate total.")