pokedex = []


def agregar_pokemon():
    print("\n--- Agregar Pokémon ---")
    nombre = input("Ingresa el nombre del Pokémon: ")
    tipo = input("Ingresa el tipo del Pokémon: ")
    
    while True:
        try:
            ps = int(input("Ingresa los PS (Puntos de Salud): "))
            break
        except ValueError:
            print("Error: Los PS deben ser un número entero. Intenta de nuevo.")
    
    pokemon = {
        "nombre": nombre,
        "tipo": tipo,
        "ps": ps
    }
    
    pokedex.append(pokemon)
    print(f"\n✓ ¡{nombre} ha sido agregado a la Pokédex!")


def ver_todos():
    print("\n--- Pokédex Completa ---")
    
    if len(pokedex) == 0:
        print("La Pokédex está vacía. ¡Agrega algunos Pokémon!")
    else:
        print(f"\nTotal de Pokémon registrados: {len(pokedex)}\n")
        for i, pokemon in enumerate(pokedex, 1):
            print(f"{i}. Nombre: {pokemon['nombre']}")
            print(f"   Tipo: {pokemon['tipo']}")
            print(f"   PS: {pokemon['ps']}")
            print("-" * 30)


def eliminar_pokemon():
    print("\n--- Eliminar Pokémon ---")
    
    if len(pokedex) == 0:
        print("La Pokédex está vacía. No hay Pokémon para eliminar.")
        return
    
    nombre_a_eliminar = input("Ingresa el nombre del Pokémon a eliminar: ")
    
    pokemon_encontrado = False
    for pokemon in pokedex:
        if pokemon["nombre"].lower() == nombre_a_eliminar.lower():
            pokedex.remove(pokemon)
            print(f"\n✓ {pokemon['nombre']} ha sido eliminado de la Pokédex.")
            pokemon_encontrado = True
            break
    
    if not pokemon_encontrado:
        print(f"\n✗ No se encontró ningún Pokémon con el nombre '{nombre_a_eliminar}'.")


def mostrar_menu():
    print("\n" + "=" * 35)
    print("**** Menú Pokédex ****")
    print("=" * 35)
    print("1. Agregar Pokémon")
    print("2. Borrar Pokémon")
    print("3. Consultar Pokédex")
    print("4. Salir")
    print("=" * 35)


def main():
    print("¡Bienvenido a tu Pokédex!")
    
    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción (1-4): ")
        
        if opcion == "1":
            agregar_pokemon()
        elif opcion == "2":
            eliminar_pokemon()
        elif opcion == "3":
            ver_todos()
        elif opcion == "4":
            print("\n¡Gracias por usar la Pokédex! ¡Hasta pronto!")
            break
        else:
            print("\n✗ Opción inválida. Por favor, selecciona una opción del 1 al 4.")


if __name__ == "__main__":
    main()
